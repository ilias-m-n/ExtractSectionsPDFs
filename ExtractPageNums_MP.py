import os
from datetime import datetime
from multiprocessing import Pool, Manager

import pandas as pd

import utility.extractor_meta as em
import utility.utility as util
from utility.Extractor import PageNumberExtractor, PageNumberExtractor_SentenceBase


def worker(input_dict, output_dict, lock, processed_section_anchors, total_count):
    while True:
        with lock:
            if not input_dict:
                break
            doc_id, doc_path = input_dict.popitem()

        result = PageNumberExtractor(doc_id=doc_id,
                                     path=doc_path,
                                     section_anchors=processed_section_anchors,
                                     min_anchor_hit_ratio=0.5,
                                     flag_only_max_hits=False,
                                     flag_allow_overlapping_sections=False,
                                     flag_adjust_real_page_num=False,
                                     flag_do_ocr=True,
                                     thresh_ocr=100,
                                     flag_allow_duplicate_hits_in_groups=True,
                                     sections_with_page_skip_groups=['auditor']
                                     ).run()

        with lock:
            output_dict[doc_id] = result
            if (len(output_dict) % 10 == 0) or (len(output_dict) == total_count):
                print(len(output_dict), '/', total_count)


def main():
    """
    directory paths
    """
    path_cwd = os.getcwd()
    path_data = os.path.join(path_cwd, 'data')
    path_input_meta = os.path.join(path_data, 'input_meta')
    path_extracted_page_nums = os.path.join(path_data, 'extracted_page_nums')

    """
    load file paths
    """
    filepath_df = pd.read_csv(os.path.join(path_input_meta, 'full_test.csv'))
    filepath_dic = {row.doc_id: row.doc_path for _, row in filepath_df.iterrows()}
    total_count = len(filepath_dic)

    """
    prepare section anchors
    """
    section_anchors = {'notes': em._notes_sections, 'auditor': em._auditor_sections}
    processed_section_anchors = util.process_section_anchors(section_anchors)
    sections = section_anchors.keys()

    """
    set up multiproessing
    """
    manager = Manager()
    input_dict = manager.dict(filepath_dic)
    output_dict = manager.dict()
    lock = manager.Lock()

    num_workers = util.get_num_workers('How many workers would you like to employ?\t',
                                       1, 36)

    with Pool(processes=num_workers) as pool:
        for _ in range(num_workers):
            pool_info = pool.apply_async(worker, args=(input_dict,
                                                       output_dict,
                                                       lock,
                                                       processed_section_anchors,
                                                       total_count))

        pool.close()
        pool.join()

    print('Workers closed.')

    output_df = pd.DataFrame(output_dict.values())

    # extract documents where algorithm failed to extract page nums for all desired sections
    mask_missing = output_df.apply(lambda row: any(len(row[section]) == 0 for section in sections), axis = 1)
    output_missing_df = output_df[mask_missing].copy()
    output_complete_df = output_df[~mask_missing].copy()
    
    output_filename = f'page_nums_{datetime.now().strftime("%y_%m_%d_%H_%M")}.parquet'
    output_missing_filename = f'page_nums_missing_{datetime.now().strftime("%y_%m_%d_%H_%M")}.parquet'
    output_complete_filename = f'page_nums_complete_{datetime.now().strftime("%y_%m_%d_%H_%M")}.parquet'
    output_df.to_parquet(os.path.join(path_extracted_page_nums, output_filename), index=False)
    output_missing_df.to_parquet(os.path.join(path_extracted_page_nums, output_missing_filename), index=False)
    output_complete_df.to_parquet(os.path.join(path_extracted_page_nums, output_complete_filename), index=False)


if __name__ == "__main__":
    main()
