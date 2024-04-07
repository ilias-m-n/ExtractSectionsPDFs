import math
import os
import re
import time
from collections import Counter
from itertools import product, combinations
from pprint import pprint
from datetime import datetime

import fitz

from . import LinkedListAnchorHitInfo as ll
from . import extractor_meta as em
from . import text_cleaning as tc
from . import utility as util



class PageTextExtractor:
    def __init__(self,
                 doc_id,
                 path,
                 section,
                 page_nums,
                 flag_reduce,
                 anchors,
                 anchor_add_word_window,
                 allowance_wildcards_reg_matches):

        self.doc_id = doc_id
        self.path = path

        self.section = section
        self.page_nums = page_nums

        self.flag_reduce = flag_reduce

        self.anchors = anchors
        self.anchor_add_word_window = anchor_add_word_window
        self.allowance_wildcards_reg_matches = allowance_wildcards_reg_matches

        self.pdf = None
        self.text = dict()
        self.text_lemma = None

        self.lemma_anchor_intervals = list()
        self.anchor_intervals_word_pos = None
        self.anchor_index_intervals = list()

        self.reduced_text = list()

    def run(self):
        self.parse_pdf()
        if self.flag_reduce:
            self.reduce_text()
        return self.return_result()

    # Read and clean PDF
    def parse_pdf(self):
        self.read_pdf()
        self.parse_pages()
        self.preprocess_text()

    def read_pdf(self):
        self.pdf = fitz.open(self.path)

    def parse_pages(self):
        for index, page in enumerate(self.pdf):
            if index in self.page_nums:
                text = page.get_text()
                self.text[index] = text

    def preprocess_text(self):
        for page_num in self.text:
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num])).split('\n\n')
            # fix split words
            self.text[page_num] = [tc.fix_split_words(para) for para in self.text[page_num]]
            # remove newline
            self.text[page_num] = [tc.remove_newline(para) for para in self.text[page_num]]
            # remove extra spaces
            self.text[page_num] = [tc.remove_extra_spaces(para) for para in self.text[page_num]]

            # self.text[page_num] = [util.full_process_text(para) for para in self.text[page_num]]
            self.text[page_num] = " ".join(self.text[page_num])

            # clean text
            self.text[page_num] = util.full_clean_text(self.text[page_num])
            self.text[page_num] = tc.clean_text(self.text[page_num])

        self.text = " ".join(self.text.values())

    def reduce_text(self):
        self.reduce_text_to_anchor_vicinities()
        self.extract_segments()

    def reduce_text_to_anchor_vicinities(self):
        self.find_anchor_intervals()
        self.fix_lemma_indeces_to_unprocessed_text()


    def find_anchor_intervals(self):
        for anchor in self.anchors:
            self.text_lemma = util.full_process_text(self.text)
            for sub_anchor in anchor:
                wild_c = str(self.allowance_wildcards_reg_matches)
                sub_anchor_pattern = re.compile(sub_anchor.replace('...', '.{,' + wild_c + '}?'))
                for match in re.finditer(sub_anchor_pattern, self.text_lemma):
                    self.lemma_anchor_intervals.append((match.start(), match.end()))
        self.lemma_anchor_intervals = self.merge_overlaying_indeces(self.lemma_anchor_intervals)



    def merge_overlaying_indeces(self, intervals):
        sorted_intervals = sorted(intervals, key=lambda x: x[0])

        merged = []

        for interval in sorted_intervals:
            # If the list of merged intervals is empty or if the current
            # interval does not overlap with the previous, simply append it.
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                # Otherwise, there is an overlap, so merge the current and previous intervals
                merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))

        return merged

    def fix_lemma_indeces_to_unprocessed_text(self):
        curr_word_index = 0
        lemma_char_pos_to_word_pos = []
        for i, c in enumerate(self.text_lemma):
            if c == " ":
                curr_word_index += 1
                lemma_char_pos_to_word_pos.append(-1)
                continue
            lemma_char_pos_to_word_pos.append(curr_word_index)
        anchor_intervals_word_pos = []
        for l_int in self.lemma_anchor_intervals:
            start = lemma_char_pos_to_word_pos[l_int[0]]
            end = lemma_char_pos_to_word_pos[l_int[1]-1] + self.anchor_add_word_window
            anchor_intervals_word_pos.append((start, end))
        anchor_intervals_word_pos = self.merge_overlaying_indeces(anchor_intervals_word_pos)
        # nnn = len(self.text.split())
        # lll = len(self.text_lemma.split())
        # if nnn != lll:
        #     print(anchor_intervals_word_pos)
        #     print(f"text number of words: {nnn}")
        #     print(f"number of words in lemma: {lll}")
        #     print()
        #     # print(self.text)
        #     print()
        #     # print(self.text_lemma)
        self.anchor_intervals_word_pos = anchor_intervals_word_pos


    def extract_segments(self):
        curr_word_index = 0
        char_pos_to_word_pos = []
        wordpos2charind = dict()
        for i, c in enumerate(self.text):
            if c == " ":
                curr_word_index += 1
                char_pos_to_word_pos.append(-1)
                continue
            wordpos2charind.setdefault(curr_word_index, []).append(i)
        for a_int in self.anchor_intervals_word_pos:
            start_char_index = wordpos2charind[a_int[0]][0]

            end_char_index = wordpos2charind[min(a_int[1], max(wordpos2charind.keys()))][-1]
            self.anchor_index_intervals.append([start_char_index, end_char_index])
            self.reduced_text.append(self.text[start_char_index:end_char_index+1])

        self.reduced_text = "\n".join(self.reduced_text)



    def return_result(self):
        if self.flag_reduce:
            c = util.count_tokens(self.reduced_text)
            print(self.reduced_text)
            return [self.reduced_text, int(c)]
        else:
            c = util.count_tokens(self.text)
            return [self.text, int(c)]


class PageNumberExtractor:

    def __init__(self,
                 doc_id,
                 path,
                 section_anchors,
                 min_anchor_occ_ratio=0,
                 flag_only_max_hits=False,
                 flag_allow_overlapping_sections=False,
                 flag_adjust_real_page_num=False):

        self.doc_id = doc_id
        self.path = path

        self.pdf = None
        self.text = dict()
        self.doc_num_pages = 0

        ########## Mode 0: extract page numbers
        self.section_anchors = section_anchors
        self.num_anchors_per_section = {key: len(anchors) for key, anchors in self.section_anchors.items()}

        self.hits_ll = dict()
        self.section_anchor_ids = {}
        self.attach_anchor_id()

        self.min_anchor_occ_ratio = min_anchor_occ_ratio
        self.min_anchor_hits = {key: math.ceil(num * self.min_anchor_occ_ratio) \
                                for key, num in self.num_anchors_per_section.items()}

        self.flag_only_max_hits = flag_only_max_hits
        self.flag_allow_overlapping_sections = flag_allow_overlapping_sections
        self.flag_adjust_real_page_num = flag_adjust_real_page_num
        self.page_num_fixer = 1 if self.flag_adjust_real_page_num else 0

        self.hits_dict = dict()

        ########## Mode 1: extract text of pages

    def run(self):
        self.parse_pdf()
        self.find_section_hits()
        self.process_results()
        return self.output_result()

    def attach_anchor_id(self):
        for section, anchors in self.section_anchors.items():
            anchor_id = 0
            self.section_anchor_ids[section] = {}
            for anchor in anchors:
                self.section_anchor_ids[section][anchor] = anchor_id
                anchor_id += 1

    # Read and clean PDF
    def parse_pdf(self):
        self.read_pdf()
        self.parse_pages()
        self.preprocess_text()

    def read_pdf(self):
        self.pdf = fitz.open(self.path)

    def parse_pages(self):
        self.doc_num_pages = len(self.pdf)
        for index, page in enumerate(self.pdf):
            self.text[index] = page.get_text()

    def preprocess_text(self):
        for page_num in self.text:
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num])).split('\n\n')
            # fix split words
            self.text[page_num] = [tc.fix_split_words(para) for para in self.text[page_num]]
            # remove newline
            self.text[page_num] = [tc.remove_newline(para) for para in self.text[page_num]]
            # remove extra spaces
            self.text[page_num] = [tc.remove_extra_spaces(para) for para in self.text[page_num]]
            # concat at newlines
            self.text[page_num] = [util.full_process_text(para) for para in self.text[page_num]]

    # find section hits
    def find_section_hits(self):
        for section, anchors in self.section_anchors.items():
            self.hits_ll[section] = ll.LinkedListAnchorHitInfo()
            for page_num in self.text:
                hits, hit_ids = self.find_anchor_hits(section, self.text[page_num], anchors)
                self.hits_ll[section].append(page_num + self.page_num_fixer, hits, hit_ids)

    def find_anchor_hits(self, section, page, anchors):
        hits = 0
        hit_ids = []
        for sub_anchor in anchors:
            flag_hit = False
            sub_anchor_patterns = [re.compile(ele.replace('...', '.*?')) for ele in sub_anchor]
            for pattern in sub_anchor_patterns:
                for line in page:
                    if re.search(pattern, line):
                        hits += 1
                        flag_hit = True
                        hit_ids.append(self.section_anchor_ids[section][sub_anchor])
                        break
                if flag_hit == True:
                    break
        return hits, set(hit_ids)

    # process hits
    def process_results(self):
        self.combine_page_groups()
        if not self.flag_allow_overlapping_sections:
            self.fix_overlaying_section()


    def combine_page_groups(self):
        for section in self.hits_ll:
            self.hits_ll[section].combine_groups()
            self.hits_ll[section].remove_below_min_hits(self.min_anchor_hits[section], self.flag_only_max_hits)
            self.hits_dict[section] = self.hits_ll[section].to_dict()

    def fix_overlaying_section(self):
        for pair in list(combinations(list(self.hits_dict.keys()), 2)):
            sections = pair
            keys = [list(self.hits_dict[section].keys()) for section in sections]
            key_combs = list(product(*keys))

            for comb in key_combs:
                if set(comb[0]).intersection(set(comb[1])):
                    val0 = self.hits_dict[pair[0]][comb[0]]
                    val1 = self.hits_dict[pair[1]][comb[1]]
                    if val0 > val1:
                        self.hits_dict[pair[1]].pop(comb[1], None)
                    elif val1 > val0:
                        self.hits_dict[pair[0]].pop(comb[0], None)


    # save results
    def output_result(self):
        result = {'doc_id': self.doc_id, 'doc_num_pages': self.doc_num_pages}
        for section in self.hits_dict:
            page_numbers = [number for tup in self.hits_dict[section].keys() for number in tup]
            result[section] = page_numbers
        return result
