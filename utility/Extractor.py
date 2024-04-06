import fitz
import os
import re
from collections import Counter
from . import extractor_meta as em
from . import text_cleaning as tc
from . import utility as util
from pprint import pprint
import math

class Extractor:

    def __init__(self, doc_id, path, section_anchors, min_anchor_occ_ratio=0, flag_only_max_hits=False):

        self.id = doc_id
        self.path = path

        self.pdf = None
        self.text = dict()
        self.text_dict = dict()

        self.section_anchors = self.process_section_anchors(section_anchors)
        self.num_anchors_per_section = {key: len(anchors) for key, anchors in self.section_anchors.items()}
        self.text_section_hits = dict()


        self.min_anchor_occ_ratio = min_anchor_occ_ratio
        self.min_anchor_hits = {key: math.ceil(num*self.min_anchor_occ_ratio) for key, num in self.num_anchors_per_section.items()}

        self.found_section_pages = {}
        self.found_section_pages_anchor_id = {}

        self.flag_only_max_hits = flag_only_max_hits

    def __str__(self):
        return f"""
        id = {self.id}"""

    def run(self):
        self.parse_pdf()
        self.find_section_hits()
        self.process_results()

    # Prep Anchors
    def process_section_anchors(self, section_anchors):
        processed_section_anchors = {}
        for section, parts in section_anchors.items():
            processed_section_anchors[section] = list()
            for part in section_anchors[section]:
                processed_part = list(set([util.full_process_text(p) for p in part]))
                processed_section_anchors[section].append(processed_part)
        return processed_section_anchors

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
            self.text_dict[index] = page.get_text("dict")

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
            # remove dots

    # find section hits
    def find_section_hits(self):
        for section, anchors in self.section_anchors.items():
            self.text_section_hits[section] = {}
            for page_num in self.text:
                self.text_section_hits[section][page_num] = self.find_anchor_hits(self.text[page_num], anchors)

    def find_anchor_hits(self, page, anchors):
        hits = 0
        for sub_anchor in anchors:
            flag_hit = False
            sub_anchor_patterns = [re.compile(ele.replace('...', '.*?')) for ele in sub_anchor]
            for pattern in sub_anchor_patterns:
                for line in page:
                    if re.search(pattern, line):
                        hits += 1
                        flag_hit = True
                        # print(pattern)
                        break
                if flag_hit == True:
                    break
        # print(hits)
        return hits

    # process hits
    def process_results(self):
        if not self.flag_only_max_hits:
            for section, hits in self.text_section_hits.items():
                self.found_section_pages[section] = {k+1:v for k, v in self.text_section_hits[section].items() if v >= self.min_anchor_hits[section]}




