import os
import sys
from datetime import datetime
from multiprocessing import Pool, Manager

import pandas as pd

import utility.extractor_meta as em
import utility.utility as util
from utility.Extractor import TermExtractor


def worker(input_dict, output_dict, lock, processed_extraction_anchors, total_count, path_current_extraction):
    while True:
        with lock:
            if not input_dict:
                break
            doc_id, row = input_dict.popitem()

        inter_res = {'doc_id': doc_id, 'doc_path': row.doc_path}

        for section in processed_extraction_anchors:

            result = TermExtractor(doc_id=doc_id,
                                   path=row.doc_path,
                                   section=section,
                                   page_nums=row[section],
                                   anchors=processed_extraction_anchors[section],
                                   anchor_add_word_window=20,
                                   allowance_wildcards_reg_matches=400,
                                   flag_capture_surrounding_sentences=True,
                                   surrounding_sentences_margin=2,
                                   flag_do_ocr=False).run()

            intervals = result[0]
            inter_file = (f'{doc_id}_{section}.txt')
            path_inter_file = os.path.join(path_current_extraction, section, inter_file)
            paragraphs = ""
            for k, interval in intervals.items():
                paragraphs += ' '.join(interval) + "\n\n"
            with open(path_inter_file, 'w', encoding='utf-8') as file:
                file.write(paragraphs)

            inter_res[f"{section}_sentences"] = result[1].values()
            inter_res[f"{section}_terms"] = result[2].values()
            inter_res[f"{section}_paragraphs_path"] = path_inter_file



        with lock:
            output_dict[doc_id] = inter_res
            if (len(output_dict) % 50 == 0) or (len(output_dict) == total_count):
                print(len(output_dict), '/', total_count)


def main():
    """
    directory paths
    """
    path_cwd = os.getcwd()
    path_data = os.path.join(path_cwd, 'data')
    path_extracted_page_nums = os.path.join(path_data, 'extracted_page_nums')
    path_extracted_text_files = os.path.join(path_data, 'extracted_text_files')
    path_current_extraction = os.path.join(path_extracted_text_files, f'run_{datetime.now().strftime("%Y%m%d-%H%M")}')
    if not os.path.exists(path_current_extraction):
        os.makedirs(path_current_extraction)
    path_output_meta = os.path.join(path_data, 'output_meta')

    """
    load meta with page nums
    """
    filepath_df = pd.read_parquet(os.path.join(path_extracted_page_nums, 'page_nums_24_04_22_02_59.parquet'))
    filepath_dic = {row.doc_id: row for _, row in filepath_df.iterrows()}
    total_count = len(filepath_dic)

    """
    prepare section anchors
    """
    extraction_anchors = {'notes': em._notes_standards, 'auditor': em._auditor_standards}
    processed_extraction_anchors = util.process_section_anchors(extraction_anchors)
    for section in extraction_anchors:
        section_path = os.path.join(path_current_extraction, section)
        if not os.path.exists(section_path):
            os.makedirs(section_path)

    """
    set up multiproessing
    """
    manager = Manager()
    input_dict = manager.dict(filepath_dic)
    output_dict = manager.dict()
    lock = manager.Lock()
    num_workers = util.get_num_workers('How many workers would you like to employ?\t',
                                       1, 10)

    with Pool(processes=num_workers) as pool:
        for _ in range(num_workers):
            pool_info = pool.apply_async(worker, args=(input_dict,
                                                       output_dict,
                                                       lock,
                                                       processed_extraction_anchors,
                                                       total_count,
                                                       path_current_extraction))

        pool.close()
        pool.join()

    print('Workers closed.')

    output_df = pd.DataFrame(output_dict.values())
    output_filename = f'extraction_{datetime.now().strftime("%y_%m_%d_%H_%M")}.parquet'
    output_df.to_parquet(os.path.join(path_output_meta, output_filename), index=False)


if __name__ == "__main__":
    main()
