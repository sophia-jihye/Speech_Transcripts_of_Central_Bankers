from config import params
import requests
from bs4 import BeautifulSoup
import time
import pickle
import re
import os
import numpy as np

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
        print(e)
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