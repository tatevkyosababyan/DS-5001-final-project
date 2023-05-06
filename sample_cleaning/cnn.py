### import utility libraries ###
import pandas as pd
import numpy as np
### import scraping packages ###
import urllib.request
import bs4
import unicodedata
### import nlp packages ###
import re
from textblob import TextBlob
### import system packages ###
from glob import glob
import time
from tqdm import tqdm
import sys
## suppress warnings ##
import warnings
warnings.filterwarnings("ignore")


try:
    ## defining file name ##
    file_path = sys.argv[1]
    print(file_path)
    file_name = file_path.split("/")[-1].split(".")[0]
    cnn = pd.read_csv(file_path).drop("Unnamed: 0", axis=1)
    sample = cnn.sample(525)
    cnn_scrape = sample[['id', 'url']]

    ### CNN Scraper
    def cnn_scraping(url):
        try:
            res_body = urllib.request.urlopen(url).read().decode("utf8")
            bs = bs4.BeautifulSoup(res_body).find_all('p', attrs={'class': "paragraph inline-placeholder"})
            article = list()
            for line in bs:
                article.append(line.text.strip())
            scraped_text = '+++'.join(article).strip()
            #time.sleep(10)
        except:
            scraped_text = '404 error'
        return scraped_text


    def scraping_function_cnn(df_cnn):
        ### scraping ###
        df_cnn['scraped'] = [str(cnn_scraping(url)) for url in tqdm(df_cnn.url.to_list())]
        return df_cnn


    df_scraped_cnn = scraping_function_cnn(cnn_scrape)
    df_scraped_cnn = df_scraped_cnn[df_scraped_cnn.scraped.str.len()>0]
    df_scraped_cnn['urlpg_subj'], df_scraped_cnn['urlpg_pola'] = [df_scraped_cnn.scraped.apply(lambda x: TextBlob(str(x)).sentiment.subjectivity),df_scraped_cnn.scraped.apply(lambda x: TextBlob(str(x)).sentiment.polarity)]
    df_scraped_cnn = df_scraped_cnn[df_scraped_cnn["scraped"]!="404 error"]

    out_folder = '/project/mechums/misinfo/url_text_mining/cnn_cnbc_fox/'
    df_scraped_cnn.to_csv(out_folder + file_name + "_out.csv")
except:
    print("Error")
    sys.exit(1)

