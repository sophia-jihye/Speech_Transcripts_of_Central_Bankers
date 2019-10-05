import os
import argparse
from datetime import datetime

bis_sleep = 0.5  # YOU CAN EDIT THIS SLEEP TIME
base_dir = os.getcwd()
print('base_dir: ', base_dir)
output_base_dir = os.path.join(base_dir, "output")

parser = argparse.ArgumentParser()
parser.add_argument('--start_page_year', type=str)  # 1997
parser.add_argument('--end_page_year', type=str)  # 2019
args = parser.parse_args()

pdf_dir = os.path.join(output_base_dir, "pdf")
pkl_dir = os.path.join(output_base_dir, "pkl")
txt_dir = os.path.join(output_base_dir, "txt")
err_dir = os.path.join(output_base_dir, "err")

params = {
    'bis_sleep': bis_sleep,
    'base_dir': base_dir,
    'output_base_dir': output_base_dir,

    'start_page_year': args.start_page_year,
    'end_page_year': args.end_page_year,

    'pdf_dir': pdf_dir,
    'pkl_dir': pkl_dir,
    'txt_dir': txt_dir,
    'err_dir': err_dir,

    'err_web2pdf_log_filepath': os.path.join(err_dir, "err_web2pdf.log"),
    'err_pdf2txt_log_filepath': os.path.join(err_dir, "err_pdf2txt.log"),
    'err_txt2csv_log_filepath': os.path.join(err_dir, "err_txt2csv.log"),
    'bis_wo_content_dict_pkl_filename_prefix': "bis_wo_content_dict_",
    'bis_w_content_csv_filepath': os.path.join(output_base_dir, "bis_w_content_FINAL.csv"),
    'bis_w_content_pkl_filepath': os.path.join(output_base_dir, "bis_w_content_FINAL.pkl")
}
