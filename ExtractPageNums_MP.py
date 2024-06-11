import os
from datetime import datetime
from multiprocessing import Pool, Manager

import pandas as pd

import utility.extractor_meta as em
import utility.utility as util
from utility.Extractor import PageNumberExtractor, PageNumberExtractor_SentenceBase


def worker(input_dict, output_dict, running_dict, lock, processed_section_anchors, total_count):
    while True:
        with lock:
            if not input_dict:
                break
            doc_id, doc_path = input_dict.popitem()
            running_dict[doc_id] = doc_path

        result = PageNumberExtractor(doc_id=doc_id,
                                     path=doc_path,
                                     section_anchors=processed_section_anchors,
                                     min_anchor_hit_ratio=0.4,
                                     flag_only_max_hits=False,
                                     flag_allow_overlapping_sections=False,
                                     flag_adjust_real_page_num=False,
                                     flag_do_ocr=True,
                                     thresh_ocr=100,
                                     flag_allow_duplicate_hits_in_groups=True,
                                     sections_do_grouping=['auditor'],
                                     sections_with_page_skip_groups=None,
                                     allowance_wildcards_reg_matches=600,
                                     ).run()

        with lock:
            output_dict[doc_id] = result
            running_dict.pop(doc_id)
            if (len(output_dict) % 10 == 0) or (len(output_dict) == total_count):
                print(len(output_dict), '/', total_count)
            if (len(running_dict) < 15):
                print(running_dict.keys())


def main():
    """
    datetime
    """
    time = datetime.now().strftime("%Y_%m_%d_%H_%M")
    
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
    path_filepath_df = util.select_file(path_input_meta, 'Select Input File')
    name_filepath_file = path_filepath_df.split('/')[-1].split('.')[0]
    filepath_df = pd.read_csv(path_filepath_df)
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
    running_dict = manager.dict()
    output_dict = manager.dict()
    lock = manager.Lock()

    num_workers = util.get_num_workers('How many workers would you like to employ?\t',
                                       1, 36)

    with Pool(processes=num_workers) as pool:
        for _ in range(num_workers):
            print('hi')
            pool_info = pool.apply_async(worker, args=(input_dict,
                                                       output_dict,
                                                       running_dict,
                                                       lock,
                                                       processed_section_anchors,
                                                       total_count))
            #print(pool_info.get())

        pool.close()
        pool.join()

    print('Workers closed.')

    output_df = pd.DataFrame(output_dict.values())

    # extract documents where algorithm failed to extract page nums for all desired sections
    mask_missing = output_df.apply(lambda row: any(len(row[section]) == 0 for section in sections), axis = 1)
    output_missing_df = output_df[mask_missing].copy()
    output_complete_df = output_df[~mask_missing].copy()
    
    output_filename = f'{name_filepath_file}_page_nums_{time}.parquet'
    output_missing_filename = f'{name_filepath_file}_page_nums_missing_{time}.parquet'
    output_complete_filename = f'{name_filepath_file}_page_nums_complete_{time}.parquet'
    output_df.to_parquet(os.path.join(path_extracted_page_nums, output_filename), index=False)
    output_missing_df.to_parquet(os.path.join(path_extracted_page_nums, output_missing_filename), index=False)
    output_complete_df.to_parquet(os.path.join(path_extracted_page_nums, output_complete_filename), index=False)


if __name__ == "__main__":
    main()
