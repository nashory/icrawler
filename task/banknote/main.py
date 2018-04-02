
import sys, os, time
import pandas as pd
import subprocess
import logging
from datetime import date
from icrawler.builtin import (BaiduImageCrawler, BingImageCrawler,
                              FlickrImageCrawler, GoogleImageCrawler,
                              GreedyImageCrawler, UrlListCrawler)


PATH = './csv_list/csv'
INPUT=['currency_korean.csv', 'currency_english.csv', 'currency_japanese.csv', 'currency_chinese.csv', 'currency_spanish.csv']
#OUTPUT_PATH = 'downloads/'
OUTPUT_PATH = 'downloads_add_krw/'
NUM_IMG = 50
#CRAWLER = ['google', 'bing', 'baidu']


def get_combination(idx):
    FULL_PATH = [ os.path.join(PATH, mfile) for mfile in INPUT ]
    keywords = []
    '''
    for f in FULL_PATH:
        data = pd.read_csv(f, skiprows=0)
        # pattern 1
        #keywords.append('{} {} {}'.format(data['name'][idx], data['magic1'][0], data['magic2'][0]))
        # pattern 2
        #keywords.append('{} {} {}'.format(data['name'][idx], data['magic1'][0], data['magic2'][1]))
        # pattern 3
        #keywords.append('{} {} {}'.format(data['name'][idx], data['magic1'][1], data['magic2'][0]))
        # pattern 4
        #keywords.append('{} {} {}'.format(data['name'][idx], data['magic1'][1], data['magic2'][1]))
        # pattern 5
        #keywords.append('{} {} {}'.format(data['country'][idx], data['magic1'][0], data['magic2'][0]))
        # pattern 6
        #keywords.append('{} {} {}'.format(data['country'][idx], data['magic1'][0], data['magic2'][1]))
        # pattern 7
        #keywords.append('{} {} {}'.format(data['country'][idx], data['magic1'][1], data['magic2'][0]))
        # pattern 8
        #keywords.append('{} {} {}'.format(data['country'][idx], data['magic1'][1], data['magic2'][1]))
        
        # pattern 1
        keywords.append('{} {}'.format(data['name'][idx], data['magic1'][0]))
        # pattern 2
        keywords.append('{} {}'.format(data['name'][idx], data['magic1'][0]))
        # pattern 3
        keywords.append('{} {}'.format(data['country'][idx], data['magic1'][1]))
        # pattern 4
        keywords.append('{} {}'.format(data['country'][idx], data['magic1'][1]))
    '''
    # for krw only.
    keywords.extend(['오천원','만원','오만원','한국 돈','한국 지폐','한국 신권','한국 구권','천원'])
    dir_name = 'KRW'
    
    #dir_name = data['code'][idx]
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

    '''
    data = pd.read_csv(os.path.join(PATH, 'currency_korean.csv'))
    length = len(data)

    # create directory beforehand.
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    for i in range(length):
        dir_name = data['code'][i]
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
    '''

    # crawl krw only.
    
    s_time = time.time()
    keywords, dir_name = get_combination(0)
    
    # create directory beforehand.
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    if not os.path.exists(os.path.join(OUTPUT_PATH, dir_name)):
        os.makedirs(os.path.join(OUTPUT_PATH, dir_name))
        
    
    # init crawler.
    google_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'google', nthreads=12)
    bing_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'bing', nthreads=12)
    baidu_crawler = init_crawler(os.path.join(OUTPUT_PATH, dir_name), 'baidu', nthreads=12)
  
    for _, v in enumerate(keywords):
        # crawl
        crawl_images(v, google_crawler, max_num=NUM_IMG, stamp='google')
        crawl_images(v, baidu_crawler, max_num=NUM_IMG, stamp='baidu')
        crawl_images(v, bing_crawler, max_num=NUM_IMG, stamp='bing')
    

