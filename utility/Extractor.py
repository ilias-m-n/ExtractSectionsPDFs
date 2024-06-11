import io
import math
import re
from itertools import product, combinations
import fitz
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Q:\Nasri\utilities\tesseract\tesseract.exe'
from PIL import Image
from . import LinkedListAnchorHitInfo as ll
from . import text_cleaning as tc
from . import utility as util


class TermExtractor:
    def __init__(self,
                 doc_id,
                 path,
                 section,
                 page_nums,
                 anchors,
                 anchor_add_word_window,
                 allowance_wildcards_reg_matches,
                 flag_capture_surrounding_sentences,
                 surrounding_sentences_margin,
                 flag_do_ocr=False,
                 thresh_ocr = 100,
                 flag_para_majority_voting=False,
                 anchors_mv=None):

        self.doc_id = doc_id
        self.path = path

        self.section = section
        self.page_nums = sorted(page_nums)

        self.anchors = anchors
        self.anchor_add_word_window = anchor_add_word_window
        self.allowance_wildcards_reg_matches = allowance_wildcards_reg_matches
        self.wild_c = str(allowance_wildcards_reg_matches)

        self.flag_capture_surrounding_sentences = flag_capture_surrounding_sentences
        self.surrounding_sentences_margin = surrounding_sentences_margin

        self.flag_do_ocr = flag_do_ocr
        self.thresh_ocr = thresh_ocr

        self.flag_para_majority_voting = flag_para_majority_voting
        self.anchors_mv = anchors_mv

        self.pdf = None
        self.text = dict()
        self.max_index_text = None
        self.text_lemma = None

        self.anchor_hits = []
        self.sentence_group_intervals = []

        self.lemma_sent_anchor_intervals = {}
        self.word_index_anchor_intervals = {}

        self.sentences = {}
        self.intervals = {}
        self.terms = {}

    def run(self):
        if len(self.page_nums) == 0:
            return self.return_results()
        self.parse_pdf()
        self.find_anchor_hits()
        self.process_anchor_hits()
        return self.return_results()

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
                if self.flag_do_ocr and len(text) < self.thresh_ocr:
                    pix = page.get_pixmap()
                    img_bytes = pix.tobytes('png')
                    img = Image.open(io.BytesIO(img_bytes))
                    # img = util.preprocess_image_for_ocr(img)
                    text = pytesseract.image_to_string(img, config="--oem 1 --psm 4")
                    self.text[index] = util.correct_text(text)
        
        

    def preprocess_text(self):
        for page_num in self.text:
            
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num]))

            """
            # fix split words
            self.text[page_num] = tc.fix_split_words(self.text[page_num])
            # remove newline
            self.text[page_num] = tc.remove_newline(self.text[page_num])
            # remove extra spaces
            self.text[page_num] = tc.remove_extra_spaces(self.text[page_num])
            # split cannot into can not
            self.text[page_num] = tc.fix_cannot(self.text[page_num])
            # fix fmancial
            self.text[page_num] = tc.fix_fmancial(self.text[page_num])
            # fix ,.
            self.text[page_num] = tc.remove_comma_dot(self.text[page_num])
            # remove roman numbers with dot
            self.text[page_num] = tc.remove_roman_num_dot(self.text[page_num])
            """
            self.text[page_num] = tc.pre_clean(self.text[page_num])

            #if page_num == 67:
            #    print(self.text[page_num])

            #print(page_num)
            #if page_num == 50:
            #    print(self.text[page_num])
            
            # fix single cap letter with dot
            self.text[page_num] = tc.remove_lonely_letterDot(self.text[page_num])
            self.text[page_num] = tc.remove_double_letterDot(self.text[page_num])
            self.text[page_num] = tc.remove_lonely_letterSpaceDot(self.text[page_num])

            # self.text[page_num] = [util.full_process_text(para) for para in self.text[page_num]]
            # self.text[page_num] = " ".join(self.text[page_num])

            # clean text
            self.text[page_num] = util.full_clean_text_keep_sent_struc(self.text[page_num])
            
            self.text[page_num] = [tc.clean_less(sent) for sent in self.text[page_num]]

            #print(page_num)
            #if page_num == 50:
            #    print(self.text[page_num])

            

        self.text = [sent for page in self.text for sent in self.text[page]]
        self.text = {index: sent for index, sent in enumerate(self.text)}
        self.max_index_text = max(self.text.keys())

    def find_anchor_hits(self):
        self.text_lemma = {key: util.full_process_text(sent) for key, sent in self.text.items()}

        for key, sent in self.text_lemma.items():
            for anchor in self.anchors:
                for sub_anchor in anchor:
                    #wild_c = str(self.allowance_wildcards_reg_matches)
                    sub_anchor_pattern = re.compile(util.prep_extract_anchors(sub_anchor, self.wild_c))

                    match = re.search(sub_anchor_pattern, sent)
                    if match is not None:
                        self.anchor_hits.append(key)
                        self.sentences[key] = self.text[key]
                        continue
                if match is not None:
                    continue

    def process_anchor_hits(self):
        if self.flag_capture_surrounding_sentences:
            self.create_anchor_hit_intervals()
        self.extract_terms()
        if self.flag_para_majority_voting and len(self.intervals) > 1:
            self.perform_mv_over_paragraphs()

    def create_anchor_hit_intervals(self):
        intervals = []
        margin = self.surrounding_sentences_margin
        for index in self.anchor_hits:
            intervals.append([max(0, index - margin), min(self.max_index_text, index + margin)])
        self.sentence_group_intervals = util.merge_overlapping_intervals(intervals)
        for interval in self.sentence_group_intervals:
            sent_group = []
            for index in range(interval[0], interval[1] + 1):
                sent_group.append(self.text[index])
            self.intervals[tuple(interval)] = sent_group

    def extract_terms(self):
        # find start and end indexes of anchor hits
        for index in self.anchor_hits:
            self.lemma_sent_anchor_intervals[index] = []
            curr = self.text_lemma[index]
            for anchor in self.anchors:
                for sub_anchor in anchor:
                    #wild_c = str(self.allowance_wildcards_reg_matches)
                    sub_anchor_pattern = re.compile(util.prep_extract_anchors(sub_anchor, self.wild_c))
                    for match in re.finditer(sub_anchor_pattern, curr):
                        self.lemma_sent_anchor_intervals[index].append((match.start(), match.end()))
                        #print(index, match.start(), match.end())
        #print('---')

        # create word pos from lemma anchor indexes
        lemma_char_pos_to_word_pos = {}
        for index in self.anchor_hits:
            #print(index)
            #print(self.text_lemma[index])
            lemma_char_pos_to_word_pos[index] = []
            curr_word_index = 0
            for i, c in enumerate(self.text_lemma[index]):
                # if lemma_char_pos_to_word_pos[index] and (
                #         lemma_char_pos_to_word_pos[index][-1] == -1 and (c == "." or c == ' ')):
                #     lemma_char_pos_to_word_pos[index].append(-1)
                #     continue
                if c == " ":
                    curr_word_index += 1
                    lemma_char_pos_to_word_pos[index].append(-1)
                    continue
                lemma_char_pos_to_word_pos[index].append(curr_word_index)
            #print(lemma_char_pos_to_word_pos[index])
            #print()

        anchor_word_pos_intervals = {}
        
        for index in self.anchor_hits:
            anchor_word_pos_intervals[index] = []
            for interval in self.lemma_sent_anchor_intervals[index]:
                start = lemma_char_pos_to_word_pos[index][interval[0]]
                end = lemma_char_pos_to_word_pos[index][interval[1] - 1]
                #print(index, start, end)
                anchor_word_pos_intervals[index].append((start, end))

        # translate word pos to char intervals in unlemmatized text
        wordpos2charindex = {}

        #print('----')

        for index in self.anchor_hits:
            curr_word_index = 0
            wordpos2charindex[index] = {}
            for i, c in enumerate(self.text[index]):
                if c == " ":
                    curr_word_index += 1
                    continue
                wordpos2charindex[index].setdefault(curr_word_index, []).append(i)

        char_pos_intervals = {}
        for index in self.anchor_hits:
            char_pos_intervals[index] = []
            self.terms[index] = []
            for interval in anchor_word_pos_intervals[index]:
                #print(index, interval[0],interval[1])
                start = wordpos2charindex[index][interval[0]][0]
                end = wordpos2charindex[index][interval[1]][-1] + 1
                char_pos_intervals[index].append((start, end))
                self.terms[index].append(self.text[index][end:])

    def perform_mv_over_paragraphs(self):
        interval_scores = {key: 0 for key in self.intervals.keys()}
        for key, interval in self.intervals.items():

            lemma_interval = [util.full_process_text(sent) for sent in interval]

            for anchor in self.anchors_mv:
                for sub_anchor in anchor:
                    sub_anchor_pattern = re.compile(util.prep_extract_anchors(sub_anchor, self.wild_c))
                    flag_hit = False
                    for sent in lemma_interval:
                        if re.search(sub_anchor_pattern, sent):
                            interval_scores[key] += 1
                            flag_hit = True
                            break
                    if flag_hit:
                        break

        # limit to majority hit intervals
        max_hit = max(interval_scores.values())
        keep_keys_intervals = [key for key, value in interval_scores.items() if value == max_hit]
        self.intervals = {key: interval for key, interval in self.intervals.items() if key in keep_keys_intervals}

        # adjust sentences and terms
        keep_keys_sent_terms = []
        for key, sentence in self.sentences.items():
            for key_interval in keep_keys_intervals:
                if key >= key_interval[0] and key <= key_interval[1]:
                    keep_keys_sent_terms.append(key)

        self.sentences = {key: sentence for key, sentence in self.sentences.items() if key in keep_keys_sent_terms}
        self.terms = {key: term for key, term in self.terms.items() if key in keep_keys_sent_terms}

    def return_results(self):
        return self.intervals, self.sentences, self.terms


class PageTextExtractor:
    def __init__(self,
                 doc_id,
                 path,
                 section,
                 page_nums,
                 flag_reduce,
                 anchors,
                 anchor_add_word_window,
                 allowance_wildcards_reg_matches,
                 flag_do_ocr=False,
                 thresh_ocr = 100,
                 testing_mode = False):

        self.doc_id = doc_id
        self.path = path

        self.section = section
        self.page_nums = page_nums

        self.flag_reduce = flag_reduce

        self.anchors = anchors
        self.anchor_add_word_window = anchor_add_word_window
        self.allowance_wildcards_reg_matches = allowance_wildcards_reg_matches
        self.wild_c = str(allowance_wildcards_reg_matches)

        self.flag_do_ocr = flag_do_ocr
        self.thresh_ocr = thresh_ocr

        self.pdf = None
        self.text = dict()
        self.text_lemma = None

        self.lemma_anchor_intervals = list()
        self.anchor_intervals_word_pos = None
        self.anchor_term_intervals_word_pos = None
        self.anchor_index_intervals = list()
        self.anchor_index_term_intervals = list()

        self.reduced_text = list()
        self.terms = list()

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
                if self.flag_do_ocr and len(text) < self.thresh_ocr:
                    pix = page.get_pixmap()
                    img_bytes = pix.tobytes('png')
                    img = Image.open(io.BytesIO(img_bytes))
                    # img = util.preprocess_image_for_ocr(img)
                    text = pytesseract.image_to_string(img, config="--oem 1 --psm 4")
                    self.text[index] = util.correct_text(text)

    def preprocess_text(self):
        for page_num in self.text:
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num]))
            # fix split words
            self.text[page_num] = tc.fix_split_words(self.text[page_num])
            # remove newline
            self.text[page_num] = tc.remove_newline(self.text[page_num])
            # remove extra spaces
            self.text[page_num] = tc.remove_extra_spaces(self.text[page_num])
            # split cannot into can not
            self.text[page_num] = tc.fix_cannot(self.text[page_num])

            # self.text[page_num] = [util.full_process_text(para) for para in self.text[page_num]]
            #self.text[page_num] = " ".join(self.text[page_num])

            # clean text
            self.text[page_num] = util.full_clean_text(self.text[page_num])
            self.text[page_num] = tc.clean_less(self.text[page_num])

        self.text = " ".join(self.text.values())

    def reduce_text(self):
        self.reduce_text_to_anchor_vicinities()
        self.extract_segments()

    def reduce_text_to_anchor_vicinities(self):
        self.find_anchor_intervals()
        self.fix_lemma_indeces_to_unprocessed_text()

    def find_anchor_intervals(self):
        self.text_lemma = util.full_process_text_keep_sentence_dots(self.text)
        # print(self.text_lemma)
        for anchor in self.anchors:

            for sub_anchor in anchor:
                #wild_c = str(self.allowance_wildcards_reg_matches)
                sub_anchor_pattern = re.compile(util.prep_extract_anchors(sub_anchor, self.wild_c))
                for match in re.finditer(sub_anchor_pattern, self.text_lemma):
                    # print(sub_anchor)
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
            if lemma_char_pos_to_word_pos and (lemma_char_pos_to_word_pos[-1] == -1 and (c == "." or c == ' ')):
                lemma_char_pos_to_word_pos.append(-1)
                continue
            if c == " ":
                curr_word_index += 1
                lemma_char_pos_to_word_pos.append(-1)
                continue
            lemma_char_pos_to_word_pos.append(curr_word_index)
        anchor_intervals_word_pos = []
        anchor_term_intervals_word_pos = []
        for l_int in self.lemma_anchor_intervals:
            start = lemma_char_pos_to_word_pos[l_int[0]]
            end = lemma_char_pos_to_word_pos[l_int[1] - 1] + self.anchor_add_word_window
            start_term = lemma_char_pos_to_word_pos[l_int[1] - 1] + 1
            end_term = end
            anchor_intervals_word_pos.append((start, end))
            anchor_term_intervals_word_pos.append((start_term, end_term))
        anchor_intervals_word_pos = self.merge_overlaying_indeces(anchor_intervals_word_pos)
        # testing
        nnn = len(self.text.split())
        lll = len(self.text_lemma.split())
        # if nnn + self.text_lemma.count(' . ') != lll:
        #     print(self.doc_id)
        #     print(anchor_intervals_word_pos)
        #     print(f"text number of words: {nnn}")
        #     print(f"number of words in lemma: {lll}")
        #     print(self.text_lemma.count(' . '))
        #     print()
        #     print(self.text)
        #     print()
        #     print(self.text_lemma)
        #     for a, b in zip(self.text.split(), self.text_lemma.split()):
        #         print(a, b)
        self.anchor_intervals_word_pos = anchor_intervals_word_pos
        self.anchor_term_intervals_word_pos = anchor_term_intervals_word_pos

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
            self.reduced_text.append(self.text[start_char_index:end_char_index + 1])

        for a_int in self.anchor_term_intervals_word_pos:
            start_char_index = wordpos2charind[a_int[0]][0]
            end_char_index = wordpos2charind[min(a_int[1], max(wordpos2charind.keys()))][-1]

            self.anchor_index_term_intervals.append([start_char_index, end_char_index])
            self.terms.append(self.text[start_char_index:end_char_index + 1])

        self.reduced_text = "\n".join(self.reduced_text)

    def return_result(self):
        if self.flag_reduce:
            c = util.count_tokens(self.reduced_text)
            return [self.reduced_text, int(c), self.terms]
        else:
            c = util.count_tokens(self.text)
            return [self.text, int(c), self.terms]


class PageNumberExtractor:

    def __init__(self,
                 doc_id,
                 path,
                 section_anchors,
                 min_anchor_hit_ratio=0,
                 flag_only_max_hits=False,
                 flag_allow_overlapping_sections=False,
                 flag_adjust_real_page_num=False,
                 flag_do_ocr=False,
                 thresh_ocr=100,
                 flag_allow_duplicate_hits_in_groups=False,
                 sections_do_grouping=None,
                 sections_with_page_skip_groups=None,
                 allowance_wildcards_reg_matches = 400,
                 testing_mode = False
                 ):

        self.doc_id = doc_id
        self.path = path

        self.pdf = None
        self.text = dict()
        self.doc_num_pages = 0

        self.section_anchors = section_anchors
        self.num_anchors_per_section = {key: len(anchors) for key, anchors in self.section_anchors.items()}

        self.hits_ll = dict()
        self.hits_ll_red = dict()
        self.section_anchor_ids = {}
        self.attach_anchor_id()

        self.min_anchor_hit_ratio = min_anchor_hit_ratio
        self.min_anchor_hits = {key: max(math.floor(num * self.min_anchor_hit_ratio), 2) \
                                for key, num in self.num_anchors_per_section.items()}

        self.flag_only_max_hits = flag_only_max_hits
        self.flag_allow_overlapping_sections = flag_allow_overlapping_sections
        self.flag_adjust_real_page_num = flag_adjust_real_page_num
        self.page_num_fixer = 1 if self.flag_adjust_real_page_num else 0
        
        self.flag_do_ocr = flag_do_ocr
        self.thresh_ocr = thresh_ocr
        
        self.flag_allow_duplicate_hits_in_groups = flag_allow_duplicate_hits_in_groups
        self.sections_do_grouping = sections_do_grouping if sections_do_grouping else []
        self.sections_with_page_skip_groups = sections_with_page_skip_groups if sections_with_page_skip_groups else []

        self.wild_c = str(allowance_wildcards_reg_matches)

        self.hits_dict = dict()

        self.testing_mode = testing_mode

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
                self.section_anchor_ids[section][anchor_id] = anchor
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
        if self.testing_mode:
            print('going in')
        for index, page in enumerate(self.pdf):
            if self.testing_mode:
                print(index)
            text = page.get_text()
            self.text[index] = text
            if self.flag_do_ocr and len(text) < self.thresh_ocr:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes('png')
                img = Image.open(io.BytesIO(img_bytes))
                # img = util.preprocess_image_for_ocr(img)
                text = pytesseract.image_to_string(img, config="--oem 1 --psm 4")
                self.text[index] = util.correct_text(text)

    def preprocess_text(self):
        for page_num in self.text:
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num]))
            # fix split words
            self.text[page_num] = tc.fix_split_words(self.text[page_num])
            # remove newline
            self.text[page_num] = tc.remove_newline(self.text[page_num])
            # remove extra spaces
            self.text[page_num] = tc.remove_extra_spaces(self.text[page_num])

            self.text[page_num] = tc.remove_spec_uni_char(self.text[page_num])
            
            # concat at newlines
            self.text[page_num] = util.full_process_text(self.text[page_num])

    # find section hits
    def find_section_hits(self):
        for section in self.section_anchors.keys():
            self.hits_ll[section] = ll.LinkedListAnchorHitInfo()
            if self.testing_mode:
                print(section)
            for page_num in self.text:
                if self.testing_mode:
                    print(page_num)
                hits, hit_ids = self.find_anchor_hits(section, self.text[page_num])
                if self.testing_mode:
                    if len(hit_ids) > 1:
                       print(page_num, hit_ids)
                    #if(page_num in [14]):
                    #   print(self.text[page_num])
                self.hits_ll[section].append(page_num + self.page_num_fixer, hits, hit_ids)

    def find_anchor_hits(self, section, page):
        hits = 0
        hit_ids = []
        for id_anchor, sub_anchor in self.section_anchor_ids[section].items():
            flag_hit = False
            
            # sub_anchor_patterns = [re.compile(ele.replace('...', '.*?')) for ele in sub_anchor]
            sub_anchor_patterns = [re.compile(util.prep_extract_anchors(ele, self.wild_c)) for ele in sub_anchor]
            for pattern in sub_anchor_patterns:
                if re.search(pattern, page):
                    #print(pattern)
                    #print(page)
                    hits += 1
                    flag_hit = True
                    hit_ids.append(id_anchor)
                    break
        return hits, set(hit_ids)

    # process hits
    def process_results(self):
        self.combine_page_groups()
        if not self.flag_allow_overlapping_sections:
            self.fix_overlaying_section()
        # self.fix_overlaying_section_ll()
        # self.combine_page_groups()

    def combine_page_groups(self):
        for section in self.hits_ll:
            if section in self.sections_do_grouping:
                self.hits_ll[section].combine_groups(self.flag_allow_duplicate_hits_in_groups)
            if section in self.sections_with_page_skip_groups:
                self.hits_ll[section].combine_skip_groups(self.flag_allow_duplicate_hits_in_groups)
            self.hits_ll[section].remove_below_min_hits(self.min_anchor_hits[section], self.flag_only_max_hits)
            self.hits_dict[section] = self.hits_ll[section].to_dict()

    def fix_overlaying_section_ll(self):
        eles = []
        for section in self.hits_ll:
            eles.append(self.hits_ll[section])
        for first in range(len(eles)):
            for second in range(first + 1, len(eles)):
                eles[first].fix_overlaying_sections(eles[second])

    def fix_overlaying_section(self):
        for pair in list(combinations(list(self.hits_dict.keys()), 2)):
            sections = pair
            keys = [list(self.hits_dict[section].keys()) for section in sections]
            key_combs = list(product(*keys))

            for comb in key_combs:
                if set(comb[0]).intersection(set(comb[1])):
                    if not (comb[0] in self.hits_dict[pair[0]] and comb[1] in self.hits_dict[pair[1]]):
                        continue
                    val0 = self.hits_dict[pair[0]][comb[0]]
                    val1 = self.hits_dict[pair[1]][comb[1]]

                    if val0 > val1:
                        val_ = self.hits_dict[pair[1]].pop(comb[1], None)
                        diff = tuple(set(comb[1]).difference(set(comb[0])))
                        self.hits_dict[pair[1]][diff] = val_
                    elif val1 > val0:
                        val_ = self.hits_dict[pair[0]].pop(comb[0], None)
                        diff = tuple(set(comb[0]).difference(comb[1]))
                        self.hits_dict[pair[0]][diff] = val_

    # save results
    def output_result(self):
        result = {'doc_id': self.doc_id, 'doc_path': self.path, 'doc_num_pages': self.doc_num_pages}
        for section in self.hits_dict:
            page_numbers = [number for tup in self.hits_dict[section].keys() for number in tup]
            result[section] = page_numbers
        return result


class PageNumberExtractor_SentenceBase:

    def __init__(self,
                 doc_id,
                 path,
                 section_anchors,
                 min_anchor_hit_ratio=0,
                 flag_only_max_hits=False,
                 flag_allow_overlapping_sections=False,
                 flag_adjust_real_page_num=False,
                 flag_do_ocr=False,
                 thresh_ocr=100,
                 flag_allow_duplicate_hits_in_groups=False,
                 sections_with_page_skip_groups=None,
                 allowance_wildcards_reg_matches = 400,):

        self.doc_id = doc_id
        self.path = path

        self.pdf = None
        self.text = dict()
        self.doc_num_pages = 0

        self.section_anchors = section_anchors
        self.num_anchors_per_section = {key: len(anchors) for key, anchors in self.section_anchors.items()}

        self.hits_ll = dict()
        self.hits_ll_red = dict()
        self.section_anchor_ids = {}
        self.attach_anchor_id()

        self.min_anchor_hit_ratio = min_anchor_hit_ratio
        self.min_anchor_hits = {key: math.ceil(num * self.min_anchor_hit_ratio) \
                                for key, num in self.num_anchors_per_section.items()}

        self.flag_only_max_hits = flag_only_max_hits
        self.flag_allow_overlapping_sections = flag_allow_overlapping_sections
        self.flag_adjust_real_page_num = flag_adjust_real_page_num
        self.page_num_fixer = 1 if self.flag_adjust_real_page_num else 0
        
        self.flag_do_ocr = flag_do_ocr
        self.thresh_ocr = thresh_ocr
        
        self.flag_allow_duplicate_hits_in_groups = flag_allow_duplicate_hits_in_groups
        self.sections_with_page_skip_groups = sections_with_page_skip_groups if sections_with_page_skip_groups else []

        self.wild_c = str(allowance_wildcards_reg_matches)

        self.hits_dict = dict()

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
            text = page.get_text()
            self.text[index] = text
            if self.flag_do_ocr and len(text) < self.thresh_ocr:
                pix = page.get_pixmap()
                img_bytes = pix.tobytes('png')
                img = Image.open(io.BytesIO(img_bytes))
                # img = util.preprocess_image_for_ocr(img)
                text = pytesseract.image_to_string(img, config="--oem 1 --psm 4")
                self.text[index] = util.correct_text(text)

    def preprocess_text(self):
        for page_num in self.text:
            # structure paragraphs
            self.text[page_num] = tc.remove_space_betw_newlines(''.join(self.text[page_num]))
            # fix split words
            self.text[page_num] = tc.fix_split_words(self.text[page_num])
            # remove newline
            self.text[page_num] = tc.remove_newline(self.text[page_num])
            # remove extra spaces
            self.text[page_num] = tc.remove_extra_spaces(self.text[page_num])
            # split cannot into can not
            self.text[page_num] = tc.fix_cannot(self.text[page_num])

            #self.text[page_num] = " ".join(self.text[page_num])

            # clean text
            self.text[page_num] = util.full_clean_text_keep_sent_struc(self.text[page_num])
            self.text[page_num] = [tc.clean_less(sent) for sent in self.text[page_num]]


    # find section hits
    def find_section_hits(self):
        for section, anchors in self.section_anchors.items():
            self.hits_ll[section] = ll.LinkedListAnchorHitInfo()
            # print(section)
            for page_num in self.text:
                hits, hit_ids = self.find_anchor_hits(section, self.text[page_num], anchors)
                # print(page_num, hit_ids)
                # if(page_num in [41]):
                #     print(self.text[page_num])
                self.hits_ll[section].append(page_num + self.page_num_fixer, hits, hit_ids)

    def find_anchor_hits(self, section, page, anchors):
        hits = 0
        hit_ids = []
        for sub_anchor in anchors:
            flag_hit = False
            # sub_anchor_patterns = [re.compile(ele.replace('...', '.*?')) for ele in sub_anchor]
            sub_anchor_patterns = [re.compile(util.prep_extract_anchors(ele, self.wild_c)) for ele in sub_anchor]
            for pattern in sub_anchor_patterns:
                for line in page:
                    if re.search(pattern, line):
                        hits += 1
                        flag_hit = True
                        hit_ids.append(self.section_anchor_ids[section][sub_anchor])
                        # print(pattern)
                        break
                if flag_hit == True:
                    break
        return hits, set(hit_ids)

    # process hits
    def process_results(self):
        self.combine_page_groups()
        if not self.flag_allow_overlapping_sections:
            self.fix_overlaying_section()
        # self.fix_overlaying_section_ll()
        # self.combine_page_groups()

    def combine_page_groups(self):
        for section in self.hits_ll:
            self.hits_ll[section].combine_groups(self.flag_allow_duplicate_hits_in_groups)
            if section in self.sections_with_page_skip_groups:
                self.hits_ll[section].combine_skip_groups(self.flag_allow_duplicate_hits_in_groups)
            self.hits_ll[section].remove_below_min_hits(self.min_anchor_hits[section], self.flag_only_max_hits)
            self.hits_dict[section] = self.hits_ll[section].to_dict()

    def fix_overlaying_section_ll(self):
        eles = []
        for section in self.hits_ll:
            eles.append(self.hits_ll[section])
        for first in range(len(eles)):
            for second in range(first + 1, len(eles)):
                eles[first].fix_overlaying_sections(eles[second])

    def fix_overlaying_section(self):
        for pair in list(combinations(list(self.hits_dict.keys()), 2)):
            sections = pair
            keys = [list(self.hits_dict[section].keys()) for section in sections]
            key_combs = list(product(*keys))

            for comb in key_combs:
                if set(comb[0]).intersection(set(comb[1])):
                    if not (comb[0] in self.hits_dict[pair[0]] and comb[1] in self.hits_dict[pair[1]]):
                        continue
                    val0 = self.hits_dict[pair[0]][comb[0]]
                    val1 = self.hits_dict[pair[1]][comb[1]]

                    if val0 > val1:
                        val_ = self.hits_dict[pair[1]].pop(comb[1], None)
                        diff = tuple(set(comb[1]).difference(set(comb[0])))
                        self.hits_dict[pair[1]][diff] = val_
                    elif val1 > val0:
                        val_ = self.hits_dict[pair[0]].pop(comb[0], None)
                        diff = tuple(set(comb[0]).difference(comb[1]))
                        self.hits_dict[pair[0]][diff] = val_

    # save results
    def output_result(self):
        result = {'doc_id': self.doc_id, 'doc_path': self.path, 'doc_num_pages': self.doc_num_pages}
        for section in self.hits_dict:
            page_numbers = [number for tup in self.hits_dict[section].keys() for number in tup]
            result[section] = page_numbers
        return result
