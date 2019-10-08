import src
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bis_speeches_text_dataset",
    version='0.1',
    author='Jihye Park',
    author_email='jihyeparkk@dm.snu.ac.kr',
    url='https://github.com/sophia-jihye/bis_speeches_text_dataset',
    description="Scraping Text Data of Central bankers' Speeches from bis.org",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords = ['bis', 'central bankers speeches'],
    packages=find_packages()
)