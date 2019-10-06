from config import params
from utils import *
from datetime import datetime

bis_sleep = params['bis_sleep']
base_dir = params['base_dir']
output_base_dir = params['output_base_dir']
pdf_dir = params['pdf_dir']
pkl_dir = params['pkl_dir']
txt_dir = params['txt_dir']
err_dir = params['err_dir']
err_web2pdf_dir = params['err_web2pdf_dir']
err_pdf2txt_dir = params['err_pdf2txt_dir']
err_txt2csv_dir = params['err_txt2csv_dir']

start_year = params['start_year']
end_year = params['end_year']

bis_wo_content_dict_pkl_filename_prefix = params['bis_wo_content_dict_pkl_filename_prefix']
bis_w_content_csv_filepath = params['bis_w_content_csv_filepath']
bis_w_content_pkl_filepath = params['bis_w_content_pkl_filepath']

create_dirs = [output_base_dir, pdf_dir, pkl_dir, txt_dir, err_dir, err_web2pdf_dir, err_pdf2txt_dir, err_txt2csv_dir]


def _get_target_url_list(start_year, end_year):
    soup = get_soup_html('https://www.bis.org/list/cbspeeches/from_01011997/index.htm')
    date_options = soup.find('select').find_all('option')

    target_year_list = list()
    for target_year in range(int(start_year), int(end_year) + 1):
        target_year_list.append(str(target_year))

    target_url_list = list()
    for opt in date_options:
        _url = opt['value']
        _year = opt['value'].split('/')[-2][-4:]
        if _year in target_year_list:
            target_url_list.append("https://www.bis.org" + _url)

    return target_url_list


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
    item_dict['title'] = get_str_strip(_a.text)
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


def main():
    start, bis_wo_content_dict = start_dict()
    target_url_list = _get_target_url_list(start_year, end_year)

    for target_url in target_url_list:
        pagenum = 0
        while True:
            pagenum += 1
            _soup_html = get_soup_html(target_url)
            sleep_(bis_sleep)

            _soup_trs = _get_trs(_soup_html)
            for _soup_tr in _soup_trs:
                _item_dict = _soup_extract_info(_soup_tr)

                # Step1) Download .pdf
                get_download(_item_dict['pdf_url'], pdf_dir, _item_dict['key'] + ".pdf")
                sleep_(bis_sleep * 0.1)
                bis_wo_content_dict[_item_dict['key']] = _item_dict

            # Page ending condition
            _next_page = _next_page_available(_soup_html)
            if not _next_page:
                print("======END PAGENUM: ", pagenum, "======")
                break

    bis_wo_content_dict_pkl_filepath = os.path.join(pkl_dir, get_str_concat(bis_wo_content_dict_pkl_filename_prefix,
                                                                            str(start_year), str(end_year)) + ".pkl")
    end_dict_pkl(start, bis_wo_content_dict, bis_wo_content_dict_pkl_filepath)


_init(create_dirs)
if __name__ == '__main__':
    main()
