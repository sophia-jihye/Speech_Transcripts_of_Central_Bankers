Central Bankers' Speeches Text Dataset

For more information, please contact me: jihyeparkk@dm.snu.ac.kr

# bis_speeches_text_dataset
Scraping Text Data of Central bankers' Speeches from bis.org

1997년부터 2019년 9월까지의 연설문 데이터 `.pdf` 파일들을 스크랩핑하여 `.txt` 파일로 변환한 결과물은 [speech_texts](https://github.com/sophia-jihye/bis_speeches_text_dataset/tree/master/speech_texts)에서 확인하실 수 있습니다.

## Introduction
Target webpage: https://www.bis.org/list/cbspeeches/from_01011997/index.htm

Target webpage에 접속하여 스크랩핑하는 대상 파일은 `.pdf` 파일이며, 스크랩핑한 `.pdf` 파일들은 `scraped_data/pdf` 디렉토리에 저장됩니다.
`.pdf` 파일로부터 텍스트를 추출하여 `.txt` 파일을 만들고 이는 `scraped_data/txt` 디렉토리에 저장됩니다. 자세한 처리과정은 아래와 같습니다.

* 위 Target webpage에 접속하여
    - HTML 정보로 출력되고 있는 메타데이터('date', 'pdf_url', 'title', 연설 장소 등이 담겨있는 'short_info')를 스크랩핑하여 Python `dict` 오브젝트에 저장합니다.
    - 메타데이터가 담긴 Python 'dict' 오브젝트를, 분기별로 그룹핑하여 `.pkl` 파일로 만들어, `scraped_data/pkl` 디렉토리에 저장합니다. (예기치 못한 네트워크 이슈로 인해 갑자기 프로세스가 중단될 경우를 대비하여 하나의 `.pkl`이 아닌 분기별 `.pkl` 파일 각각 저장되도록 하였습니다.)
    - `.pdf` 포맷으로 공개되어있는 연설문 텍스트 데이터를 스크랩핑하고, 스크랩핑한 `.pdf` 파일들을 `scraped_data/pdf` 디렉토리에 저장합니다.
* `scraped_data/pkl` 디렉토리 내에 있는 `.pkl` 파일들을 모두 merge하여 하나의 최종 Python 'dict' 오브젝트로 만듭니다.
* `scraped_data/pdf` 디렉토리 내 `.pdf` 파일을 하나씩 처리하며 텍스트를 추출하여
    - 추출한 텍스트를, `scraped_data/txt` 디렉토리 내에 `.txt` 파일로 저장합니다.
    - 추출한 텍스트를, 이전에 merge하여 만든 최종 Python 'dict' 오브젝트에 업데이트합니다.
* 최종 Python 'dict' 오브젝트를
    - `scraped_data/bis_w_content_FINAL.csv`로 저장합니다. 
    - 해당 csv에 저장되어 있는 데이터는 아래와 같은 내용을 저장하고 있습니다. 
        - key : `scraped_data/pdf` 또는 `scraped_data/txt` 디렉토리 내 파일명과 매칭할 수 있는 key입니다.
        - date : Target webpage에 게재된 메타정보로서, 해당 연설문이 Target webpage에 업로드된 날짜입니다.
        - pdf\_url : Target webpage에 게재된 메타정보로서, 해당 연설문 데이터에 대한 .pdf 파일을 스크랩핑할 때 방문한 url입니다. 
        - title : Target webpage에 게재된 메타정보로서, 해당 연설문의 제목입니다.
        - short\_info : Target webpage에 게재된 메타정보로서, 연설자가 연설을 한 '장소', '날짜' 등의 정보를 담고있는 2-3 문장의 텍스트입니다.
        - content: 해당 연설문 .pdf 파일로부터 추출한 텍스트입니다.   
        
        
| key           | date            | pdf\_url         | title          | short\_info        | content       |
|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|:---------------:|
| r970106         | 1997-01-06      | https://www.bis.org/review/r970106.pdf | Prof. Tietmeyer discusses the Bundesbank's commitment to .. | Translation of an article by the President of the Deutsche Bundesbank .. | Prof. Tietmeyer discusses the Bundesbank’s commitment to .. |
| ... | ... | ... | ... | ... | ... |

## Folder structure
The following shows basic folder structure.
```
├── setup.py
├── src
│   ├── main.py
│   ├── config.py
│   ├── utils.py
├── scraped_data
│   ├── pdf
│        ├── r970326a.pdf
│        ├── r970326b.pdf
│        ├── ...
│   ├── txt
│        ├── r970326a.txt
│        ├── r970326b.txt
│        ├── ...
│   ├── pkl
│        ├── bis_wo_content_dict_1997_1Q_Jan-Mar.pkl
│        ├── bis_wo_content_dict_1997_2Q_Apr-jun.pkl
│        ├── ...
│   ├── err
│        ├── web2pdf
│             ├── r970326b.log   # If an error occurrs while parsing data from web to .pdf, .log file is created.
│             ├── ...
│        ├── pdf2txt
│             ├── r970326c.log   # If an error occurrs while parsing data from .pdf to .txt, .log file is created.
│             ├── ...
│   ├── 20191007-00-59-59.log   # If an unexpecteed error orrcus, .log file is created.
│   ├── bis_w_content_FINAL.csv
│   ├── bis_w_content_FINAL.pkl

```

## Development Environment
* Ubuntu 16.04.6 LTS
* Python 3.6.9
* pdfminer 2.1.0
* beautifulsoup4 4.5.3
* requests 2.22.0
* argparse 1.4.0
* datetime 1.0.0
* numpy 1.15.4

## Install
##### 0-1. Clone this repository.
```sh
git clone https://github.com/sophia-jihye/bis_speeches_text_dataset.git
```

##### 0-2. You can download necessary packages by running `setup.py`
```sh
python setup.py install
```


##### 1. You can set the `sleep` time and `output` directory path at `src/config.py`.
```python
bis_sleep = 0.5  # YOU CAN EDIT THIS SLEEP TIME

output_base_dir = os.path.join(base_dir, "output")   # YOU CAN EDIT THIS OUTPUT DIRECTORY PATH
```

##### 2. Run `src/main.py`.
If you want to scrape data of whole range, just run `main.py` without any aruments, as below.
```sh
cd bis_speeches_text_dataset
python src/main.py
```

If you want to scrape data of specific range, run `main.py` with arguments `--start_year`, and `--end_year`.
For your information, the data listed on bis.org starts from 1997 to today.
```sh
cd bis_speeches_text_dataset
python src/main.py --start_year 1997 --end_year 1998   # It scrapes data of 1997 and 1998.
```
