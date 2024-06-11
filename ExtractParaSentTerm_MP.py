import os
import sys
from datetime import datetime
from multiprocessing import Pool, Manager
import json

import pandas as pd

import utility.extractor_meta as em
import utility.utility as util
from utility.Extractor import TermExtractor


def worker(input_dict, output_dict, lock, processed_extraction_anchors, flag_mv, processed_mv_anchors,
           total_count, path_current_extraction):
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
                                   allowance_wildcards_reg_matches=600,
                                   flag_capture_surrounding_sentences=True,
                                   surrounding_sentences_margin=2,
                                   flag_do_ocr=True,
                                   thresh_ocr = 100,
                                   flag_para_majority_voting=flag_mv[section],
                                   anchors_mv=processed_mv_anchors[section]).run()

            intervals = result[0]
            inter_file = (f'{doc_id}_{section}.txt')
            path_inter_file = os.path.join(path_current_extraction, section, inter_file)
            paragraphs = ""
            for k, interval in intervals.items():
                paragraphs += ' '.join(interval) + "\n\n"
            with open(path_inter_file, 'w', encoding='utf-8') as file:
                file.write(paragraphs)

            sentences = json.dumps(result[1])
            terms = json.dumps(result[2])


            inter_res[f"{section}_sentences"] = sentences
            inter_res[f"{section}_terms"] = terms
            inter_res[f"{section}_path"] = path_inter_file



        with lock:
            output_dict[doc_id] = inter_res
            if (len(output_dict) % 50 == 0) or (len(output_dict) == total_count):
                print(len(output_dict), '/', total_count)

def extract_gpt_meta(df, section, path_gpt_meta, time):
    gpt_meta = df[['doc_id', f'{section}_path']].copy()
    gpt_meta.rename(columns={f'{section}_path': 'doc_path'}, inplace=True)
    gpt_meta.to_csv(os.path.join(path_gpt_meta, f'{section}_gptmeta_{time}.csv'), index=False)

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
    path_extracted_page_nums = os.path.join(path_data, 'extracted_page_nums')
    path_extracted_text_files = os.path.join(path_data, 'extracted_text_files')
    path_output_meta = os.path.join(path_data, 'output_meta')
    

    """
    load meta with page nums
    """
    
    #filepath_df = pd.read_parquet(os.path.join(path_extracted_page_nums, 'page_nums_complete_24_04_26_15_06.parquet'))
    path_filepath_df = util.select_file(path_extracted_page_nums, 'Select Input File')
    name_filepath_file = "_".join(path_filepath_df.split('/')[-1].split('_')[:-8])
    filepath_df = pd.read_parquet(path_filepath_df)
    filepath_dic = {row.doc_id: row for _, row in filepath_df.iterrows()}
    total_count = len(filepath_dic)

    # file dependent paths
    path_current_extraction = os.path.join(path_extracted_text_files, f'{name_filepath_file}_{time}')
    if not os.path.exists(path_current_extraction):
        os.makedirs(path_current_extraction)
    path_gpt_meta = os.path.join(path_data, 'gpt_meta', f'{name_filepath_file}_{time}')
    if not os.path.exists(path_gpt_meta):
        os.makedirs(path_gpt_meta)

    """
    prepare section and mv anchors
    """
    extraction_anchors = {'notes': em._notes_standards, 'auditor': em._auditor_standards}
    processed_extraction_anchors = util.process_section_anchors(extraction_anchors)
    sections = extraction_anchors.keys()
    mv_anchors = {'notes': em._notes_sections, 'auditor': em._auditor_sections}
    processed_mv_anchors = util.process_section_anchors(mv_anchors)
    flag_mv = {'auditor': False, 'notes': False}

    """
    prepare folders
    """
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
                                       1, 36)

    with Pool(processes=num_workers) as pool:
        for _ in range(num_workers):
            print('hi')
            pool_info = pool.apply_async(worker, args=(input_dict,
                                                       output_dict,
                                                       lock,
                                                       processed_extraction_anchors,
                                                       flag_mv,
                                                       processed_mv_anchors,
                                                       total_count,
                                                       path_current_extraction))
            #print(pool_info.get())
            

        pool.close()
        pool.join()

    print('Workers closed.')


    output_df = pd.DataFrame(output_dict.values())

    # exctract documents from which we were unable to extract terms or their sections
    mask_missing = output_df.apply(lambda row: any(row[f'{section}_sentences'] == '{}' for section in sections), axis=1)
    output_missing_df = output_df[mask_missing].copy()
    output_complete_df = output_df[~mask_missing].copy()
    
    output_filename = f'extraction_{name_filepath_file}_{time}.parquet'
    output_missing_filename = f'extraction_{name_filepath_file}_missing_{time}.parquet'
    output_complete_filename = f'extraction_{name_filepath_file}_complete_{time}.parquet'
    
    output_df.to_parquet(os.path.join(path_output_meta, output_filename), index=False)
    output_missing_df.to_parquet(os.path.join(path_output_meta, output_missing_filename), index=False)
    output_complete_df.to_parquet(os.path.join(path_output_meta, output_complete_filename), index=False)

    # create gpt meta input
    for section in extraction_anchors.keys():
        extract_gpt_meta(output_complete_df, section, path_gpt_meta, time)


if __name__ == "__main__":
    main()
