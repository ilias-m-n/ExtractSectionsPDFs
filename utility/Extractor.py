import math
import os
import re
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
                 path,):

        self.doc_id = doc_id
        self.path = path

        self.pdf = None
        self.text = dict()

    def run(self):
        pass

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

        ########## Mode 0: extract page numbers
        self.section_anchors = self.process_section_anchors(section_anchors)
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

    # Prep Anchors
    def process_section_anchors(self, section_anchors):
        processed_section_anchors = {}
        for section, parts in section_anchors.items():
            processed_section_anchors[section] = list()
            for part in section_anchors[section]:
                processed_part = tuple([util.full_process_text(p) for p in part])
                processed_section_anchors[section].append(processed_part)
        return processed_section_anchors

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
        result = {'doc_id': self.doc_id}
        for section in self.hits_dict:
            page_numbers = [number for tup in self.hits_dict[section].keys() for number in tup]
            result[section] = page_numbers
        return result
