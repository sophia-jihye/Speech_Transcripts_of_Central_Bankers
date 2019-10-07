from config import params
import requests
from bs4 import BeautifulSoup
import time
import pickle
import re
import os
import numpy as np
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator
import csv

unexpected_errlog_filepath = params['unexpected_errlog_filepath']


def write_errlog(errlog_filepath, content):
    text_file = open(errlog_filepath, "w", encoding='utf-8')
    text_file.write(content)
    text_file.close()
    print("Error occurred: ", errlog_filepath)


def get_soup_html(url):
    try:
        resp = requests.get(url)
        soup_html = BeautifulSoup(resp.content, 'html.parser')
    except Exception as e:
        print(str(e))
        content = "get_soup_html" + "\n" + url + "\n"
        write_errlog(unexpected_errlog_filepath, content)
    return soup_html


def sleep_(config_sleep, random=True):
    if random:
        sleeptime = np.random.randint(1, 10) * config_sleep
    else:
        sleeptime = config_sleep
    print('sleep ', sleeptime)
    time.sleep(sleeptime)


def start_dict():
    start = time.time()
    _dict = dict()
    return start, _dict


def end_dict_pkl(start, dict_to_save, pkl_path):
    with open(pkl_path, 'wb') as f:
        pickle.dump(dict_to_save, f)
    print('Creating .pkl completed: ', pkl_path)

    print('===== Total number of items without overlapping = ', len(dict_to_save.keys()))

    elapsed_time = time.time() - start
    elapsed_time_format = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print('END. Elapsed time: ', elapsed_time_format)


normalize_pattern = re.compile('[\n\t]')
doublespace_pattern = re.compile('\s+')


def get_str_strip(content, without_n_t_blank=False):
    if content is None:
        val = ''
    else:
        val = str(content).strip()
        if without_n_t_blank:
            val = normalize_pattern.sub(' ', val)
            val = doublespace_pattern.sub(' ', val)
    return val


def get_str_concat(*args):
    _str = ""
    firstLine = True
    for idx, arg in enumerate(args):
        if idx == 0:
            _str += arg
            firstLine = False
            continue
        _str = _str + "_" + arg
    return _str


def get_download(file_url, download_dir, fname):
    r = requests.get(file_url, stream=True)
    download_path = os.path.join(download_dir, fname)
    with open(download_path, "wb") as f:
        f.write(r.content)
    print('Downloading completed: ', download_path)


def get_filepaths(directory, file_ext):
    filepaths = []
    for r, d, f in os.walk(directory):
        for file in f:
            if file_ext in file:
                filepaths.append(os.path.join(r, file))
    return filepaths


def merge_pkl2dict(filepaths):
    whole_dict = dict()
    for filepath in filepaths:
        with open(filepath, 'rb') as f:
            current_dict = pickle.load(f)
            whole_dict.update(current_dict)
    return whole_dict


def pdf2txt(one_file, txt_dir, target_regex=None):
    password = ""

    fp = open(one_file, "rb")
    parser = PDFParser(fp)
    document = PDFDocument(parser, password)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    whole_extracted_text = ""
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text = lt_obj.get_text()
                if target_regex is not None:
                    target_content = target_regex.sub(' ', extracted_text)
                else:
                    target_content = extracted_text
                whole_extracted_text += target_content
    fp.close()
    return whole_extracted_text


def save_txt(txt_filepath, content):
    with open(txt_filepath, "w", encoding='utf-8') as txt_output:
        txt_output.write(content)
    print('Creating txt_file completed: ', txt_filepath)


def write_dict2csv(item_dict, csv_filepath, column_list, csv_delimiter=','):
    f = open(csv_filepath, 'w', encoding='utf-8-sig', newline='')
    wr = csv.writer(f, delimiter=csv_delimiter)
    wr.writerow(column_list)
    for _key in sorted(item_dict.keys()):
        _item = item_dict[_key]
        row_val_list = list()
        for _subkey in column_list:
            if _subkey not in _item.keys():
                _item[_subkey] = ''

            row_val_list.append(_item[_subkey].replace(',', ' '))

        wr.writerow(row_val_list)
    f.close()
    print('Creating .csv file completed: ', csv_filepath)
