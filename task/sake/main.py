
import sys, os, time
import pandas as pd
import subprocess
import logging
from datetime import date
from icrawler.builtin import (BaiduImageCrawler, BingImageCrawler,
                              FlickrImageCrawler, GoogleImageCrawler,
                              GreedyImageCrawler, UrlListCrawler)


PATH = './csv_list'
INPUT=['sake_japanese.csv', 'sake_korean.csv']
OUTPUT_PATH = 'downloads/'
NUM_IMG = 50
#CRAWLER = ['google', 'bing', 'baidu']

def get_combination(idx):
    FULL_PATH = [ os.path.join(PATH, mfile) for mfile in INPUT ]
    keywords = []
    for f in FULL_PATH:
        data = pd.read_csv(f, skiprows=0)
  
        # pattern 1
        #keywords.append('{} {}'.format(data['origin'][idx].replace(',', ' '), data['name'][idx].replace(',',' ')))
        # pattern 2
        #keywords.append('{} {}'.format(data['made_by'][idx].replace(',', ' '), data['name'][idx].replace(',',' ')))
        # pattern 3
        keywords.append('{}'.format(data['name'][idx].replace(',',' ')))
        
        dir_name = str(idx)
        return keywords, dir_name


def init_crawler(path, crawler=None, nthreads=4):
    assert crawler!=None, 'crawler is set as None.'
    if crawler in ['google']:
        m_crawler = GoogleImageCrawler(
                                downloader_threads=nthreads,
                                storage = {'root_dir': path},
                                log_level = logging.INFO)
    elif crawler in ['bing']:
        m_crawler = BingImageCrawler(
                                storage = {'root_dir': path},
                                log_level = logging.INFO)
    elif crawler in ['baidu']:
        m_crawler = BaiduImageCrawler(
                                downloader_threads=nthreads,
                                storage = {'root_dir': path}) 
    return m_crawler


def crawl_images(keyword, crawler=None, max_num=10, stamp='None'):
    assert crawler!=None, 'crawler is set as None.'
    logging.info('[{}] searching by keyword: {}'.format(stamp, keyword))
    crawler.crawl(keyword, max_num=max_num)




if __name__=="__main__":

    data = pd.read_csv(os.path.join(PATH, 'sake_korean.csv'))
    length = len(data)

    # create directory beforehand.
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    for i in range(length):
        dir_name = str(i)
        if not os.path.exists(os.path.join(OUTPUT_PATH, dir_name)):
            os.makedirs(os.path.join(OUTPUT_PATH, dir_name))
    
    # crawl data.
    for i in range(length): 
        s_time = time.time()
        keywords, dir_name = get_combination(i)
    
        # init crawler.
        google_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'google', nthreads=12)
        bing_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'bing', nthreads=12)
        baidu_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'baidu', nthreads=12)
  
        for _, v in enumerate(keywords):
            # crawl
            crawl_images(v, google_crawler, max_num=NUM_IMG, stamp='google')
            crawl_images(v, baidu_crawler, max_num=NUM_IMG, stamp='baidu')
            crawl_images(v, bing_crawler, max_num=NUM_IMG, stamp='bing')
        logging.info('==> [{}/{}] completed.'.format(i+1, length))


