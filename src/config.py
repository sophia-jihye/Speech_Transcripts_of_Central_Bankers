import os
from collections import namedtuple
from datetime import datetime

# user configuration
bis_sleep = 0.5

# system configuration
base_dir = os.path.dirname(os.path.abspath(__file__))
output_base_dir = os.path.join(base_dir, 'scraped_data')
start_year = 1997
end_year = datetime.today().year

class Parameters:
    def __init__(self):
        self.bis_sleep = bis_sleep
        self.base_dir = base_dir
        self.output_base_dir = output_base_dir
        self.start_year = start_year
        self.end_year = end_year
        self.pdf_dir = os.path.join(output_base_dir, "pdf")
        self.pkl_dir = os.path.join(output_base_dir, "pkl")
        self.txt_dir = os.path.join(output_base_dir, "txt")
        self.err_dir = os.path.join(output_base_dir, "err")
        self.err_web2pdf_dir = os.path.join(self.err_dir, "web2pdf")
        self.err_pdf2txt_dir = os.path.join(self.err_dir, "pdf2txt")
        self.bis_wo_content_dict_pkl_filename_prefix = "bis_wo_content_dict"
        self.bis_w_content_csv_filepath = os.path.join(
            output_base_dir, "bis_w_content_FINAL.csv")
        self.unexpected_errlog_filepath = os.path.join(
            output_base_dir, datetime.now().strftime("%Y%m%d-%H-%M-%S") + ".log")

    def __str__(self):
        item_strf = ['{} = {}'.format(attribute, value) for attribute, value in self.__dict__.items()]
        strf = 'Parameters(\n  {}\n)'.format('\n  '.join(item_strf))
        return strf

parameters = Parameters()
print(parameters)
