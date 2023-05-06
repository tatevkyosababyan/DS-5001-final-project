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
    cnbc = pd.read_csv(file_path).drop("Unnamed: 0", axis=1)
    sample = cnbc.sample(500)
    cnbc_scrape = sample[['id', 'url']]

    ### CNBC Scraper
    def cnbc_scraping(url):
        try:
            res_body = urllib.request.urlopen(url).read().decode("utf8")
            bs = bs4.BeautifulSoup(res_body).find_all('p')
            article = list()
            for line in bs:
                article.append(line.text)#.strip()
            if (article[0]=='Credit Cards'):
                article = article[111:]
            article = article[:-6]
            scraped_text = "+++".join(article)
            scraped_text = unicodedata.normalize("NFKD", scraped_text)
            scraped_text = scraped_text.replace('\\', '').replace('\'', '')
            #time.sleep(10)
        except:
            scraped_text = '404 error'
            print("404 error at " + str(url))
        return scraped_text


    def scraping_function_cnbc(df_cnbc):
        ### scraping ###
        df_cnbc['scraped'] = [str(cnbc_scraping(url)) for url in tqdm(df_cnbc.url.to_list())]
        return df_cnbc


    df_scraped = scraping_function_cnbc(cnbc_scrape)
    df_scraped = df_scraped[df_scraped.scraped.str.len()>0]
    df_scraped['urlpg_subj'], df_scraped['urlpg_pola'] = [df_scraped.scraped.apply(lambda x: TextBlob(str(x)).sentiment.subjectivity), df_scraped.scraped.apply(lambda x: TextBlob(str(x)).sentiment.polarity)]



    out_folder = '/project/mechums/misinfo/url_text_mining/cnn_cnbc_fox/'
    df_scraped.to_csv(out_folder + file_name + "_out.csv")

except:
    print("Error")
    sys.exit(1)

