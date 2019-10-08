import os
import argparse
from datetime import datetime

bis_sleep = 0.5  # YOU CAN EDIT THIS SLEEP TIME
base_dir = os.path.realpath(os.getcwd())
print('base_dir: ', base_dir)
output_base_dir = os.path.join(base_dir, "output")   # YOU CAN EDIT THIS OUTPUT DIRECTORY PATH

parser = argparse.ArgumentParser()
parser.add_argument('--start_year', type=int, default=1997)  # 1997
parser.add_argument('--end_year', type=int, default=datetime.today().year)  # 2019
args = parser.parse_args()

pdf_dir = os.path.join(output_base_dir, "pdf")
pkl_dir = os.path.join(output_base_dir, "pkl")
txt_dir = os.path.join(output_base_dir, "txt")
err_dir = os.path.join(output_base_dir, "err")
err_web2pdf_dir = os.path.join(err_dir, "web2pdf")
err_pdf2txt_dir = os.path.join(err_dir, "pdf2txt")

params = {
    'bis_sleep': bis_sleep,
    'base_dir': base_dir,
    'output_base_dir': output_base_dir,

    'start_year': args.start_year,
    'end_year': args.end_year,

    'pdf_dir': pdf_dir,
    'pkl_dir': pkl_dir,
    'txt_dir': txt_dir,
    'err_dir': err_dir,
    'err_web2pdf_dir': err_web2pdf_dir,
    'err_pdf2txt_dir': err_pdf2txt_dir,

    'bis_wo_content_dict_pkl_filename_prefix': "bis_wo_content_dict",
    'bis_w_content_csv_filepath': os.path.join(output_base_dir, "bis_w_content_FINAL.csv"),
    'bis_w_content_pkl_filepath': os.path.join(output_base_dir, "bis_w_content_FINAL.pkl"),
    'unexpected_errlog_filepath': os.path.join(output_base_dir, datetime.now().strftime("%Y%m%d-%H-%M-%S") + ".log")
}
