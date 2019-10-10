from config import parameters
from utils import *
from datetime import datetime
import time
import os
import re

bis_sleep = parameters.bis_sleep
base_dir = parameters.base_dir
output_base_dir = parameters.output_base_dir
pdf_dir = parameters.pdf_dir
pkl_dir = parameters.pkl_dir
txt_dir = parameters.txt_dir
err_dir = parameters.err_dir
err_web2pdf_dir = parameters.err_web2pdf_dir
err_pdf2txt_dir = parameters.err_pdf2txt_dir

start_year = parameters.start_year
end_year = parameters.end_year

bis_wo_content_dict_pkl_filename_prefix = parameters.bis_wo_content_dict_pkl_filename_prefix
bis_w_content_csv_filepath = parameters.bis_w_content_csv_filepath

create_dirs = [output_base_dir, pdf_dir, pkl_dir, txt_dir, err_dir, err_web2pdf_dir, err_pdf2txt_dir]


def _get_target_url_dict(start_year, end_year, already_scraped_pdf_files):
    already_scraped_year = None
    if len(already_scraped_pdf_files) > 0:
        already_scraped_pdf_files.sort(key=os.path.getmtime)
        most_recently_scraped_filepath = already_scraped_pdf_files[-1]
        print('most recently scraped file: ', most_recently_scraped_filepath)
        
        _year_two_digits = os.path.basename(most_recently_scraped_filepath)[1:3]        
        if _year_two_digits in ['97', '98', '99']:
            already_scraped_year = int(_year_two_digits) + 1900
        else:
            already_scraped_year = int(_year_two_digits) + 2000
        
    quarter_dict = {'jan': '1Q', 'apr': '2Q', 'jul': '3Q', 'oct': '4Q'}

    soup = get_soup_html('https://www.bis.org/list/cbspeeches/from_01011997/index.htm')
    date_options = soup.find('select').find_all('option')

    target_year_list = list()
    for target_year in range(start_year, end_year + 1):
        if already_scraped_year is not None and target_year < already_scraped_year:
            continue
        target_year_list.append(str(target_year))

    target_url_dict = dict()
    for opt in date_options:
        _url = opt['value']
        _year = opt['value'].split('/')[-2][-4:]
        if _year in target_year_list:
            months_str = opt.text[:-4].strip()
            quarter_str = "_" + quarter_dict[months_str[:3].lower()] + "_"
            _key = opt.text[-4:] + quarter_str + months_str
            target_url_dict[_key] = "https://www.bis.org" + _url

    return target_url_dict


def _get_target_url_with_pagenum(target_url_prefix, pagenum):
    target_url = target_url_prefix + "/page_" + str(pagenum) + ".htm"
    print(target_url)
    return target_url


def _get_trs(soup_html):
    table = soup_html.find("table", {"class": "documentList"})
    trs = table.find('tbody').find_all('tr')
    print('# of documents: ', len(trs))
    return trs


def _next_page_available(soup_html):
    li_next = soup_html.find("li", {"class": "next"})
    if li_next is None:
        return False

    if li_next.get('title') is None:
        return True
    else:
        return False


def _soup_extract_info(tr):
    item_dict = dict()

    _item_date = tr.find("td", {"class": "item_date"})
    _date = get_str_strip(_item_date.text)
    if _date != '':
        datetime_object = datetime.strptime(_date, '%d %b %Y')
        item_dict['date'] = datetime_object.strftime("%Y-%m-%d")

    _a = tr.find("div", {"class": "title"}).find('a')
    item_dict['title'] = get_str_strip(_a.text, without_n_t_blank=True)
    item_dict['pdf_url'] = "https://www.bis.org" + _a['href'][:-4] + ".pdf"
    item_dict['key'] = item_dict['pdf_url'].split('/')[-1][:-4]

    try:
        _item_short_info = tr.find("div", {"class": "info"}).text
        item_dict['short_info'] = get_str_strip(_item_short_info, without_n_t_blank=True)
    except Exception as e:
        item_dict['short_info'] = ''

    return item_dict


def _init(dirs):
    # create dirs
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

    column_list = ['key', 'date', 'pdf_url', 'title', 'short_info', 'content']
    wo_special_char_regex = re.compile('^[\W_]+$')
    return column_list, wo_special_char_regex


def main():
    already_scraped_pdf_files = get_filepaths(pdf_dir, '.pdf')
    target_url_dict = _get_target_url_dict(start_year, end_year, already_scraped_pdf_files)

    # Step1) Download .pdf
    for target_range_str in sorted(target_url_dict.keys()):
        _target_url = target_url_dict[target_range_str]
        print("===", target_range_str, "\t", _target_url, "===")
        start, bis_wo_content_dict = start_dict()

        pagenum = 0
        while True:
            pagenum += 1
            target_url = _get_target_url_with_pagenum(_target_url, pagenum)
            print('pagenum:', str(pagenum), '=>', target_url)

            _soup_html = get_soup_html(target_url)
            sleep_(bis_sleep)

            _soup_trs = _get_trs(_soup_html)
            for _soup_tr in _soup_trs:
                _item_dict = _soup_extract_info(_soup_tr)

                try:
                    get_download(_item_dict['pdf_url'], pdf_dir, _item_dict['key'] + ".pdf")
                except Exception as e:
                    print(str(e))
                    write_errlog(os.path.join(err_web2pdf_dir, _item_dict['key'] + '.log'), str(e))
                    continue

                sleep_(bis_sleep * 0.1)
                bis_wo_content_dict[_item_dict['key']] = _item_dict

            # Page ending condition
            _next_page = _next_page_available(_soup_html)
            if not _next_page:
                print("======END PAGENUM: ", pagenum, "======")
                break

        bis_wo_content_dict_pkl_filepath = os.path.join(pkl_dir, get_str_concat(bis_wo_content_dict_pkl_filename_prefix,
                                                                                str(target_range_str)) + ".pkl")
        end_dict_pkl(start, bis_wo_content_dict, bis_wo_content_dict_pkl_filepath)

    # Step2) .pdf -> .txt
    start = time.time()
    pkl_filepaths = get_filepaths(pkl_dir, '.pkl')
    pdf_filepaths = get_filepaths(pdf_dir, '.pdf')
    bis_w_content_dict = merge_pkl2dict(pkl_filepaths)

    count = 0
    for one_file in pdf_filepaths:
        count += 1
        print("[", count, "/", len(pdf_filepaths), "]")
        filename_w_ext = os.path.basename(one_file)
        filename_only = filename_w_ext[:-4]
        try:
            _whole_txt = pdf2txt(one_file, txt_dir, wo_special_char_regex)
            bis_w_content_dict[filename_only]['content'] = get_str_strip(_whole_txt, without_n_t_blank=True)
        except Exception as e:
            print(str(e))
            write_errlog(os.path.join(err_pdf2txt_dir, filename_only + '.log'), str(e))
            continue

        save_txt(os.path.join(txt_dir, filename_only + ".txt"), _whole_txt)

    # Step3) *FINAL.pkl -> .csv
    write_dict2csv(bis_w_content_dict, bis_w_content_csv_filepath, column_list)
    os.system('rm -rf ' + pkl_dir)

column_list, wo_special_char_regex = _init(create_dirs)
if __name__ == '__main__':
    main()