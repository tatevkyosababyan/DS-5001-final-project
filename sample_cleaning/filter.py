### import utility libraries ###
import pandas as pd
import numpy as np
### import os libraries ###
import sys
path = sys.argv[1]
print(path) ### print input path in .out name for validation
def filter_df(filename):
    df = pd.read_csv(filename) ### Read DF
    df["url"] = 'https://' + df.url_host.astype('str') + '/' + df.url_dir.astype('str') + '/' + df.url_page.astype('str') ### Make URL
    df['year_month'] = ['-'.join(date.split('-')[0:2]) for date in df.tdate.to_list()] ### Make Year Month
    df = df[(df.year_month == '2020-09')|(df.year_month == '2020-10') | (df.year_month == '2020-11')|(df.year_month == '2020-12')] ### Filter for Month-Year (10-11)
    ## Filter for Scrapeable Domain 
    ### Exclude Fox News Elections ###
    fox_election_boolean = pd.Series([url.split('/')[3]!='elections' for url in df[df.domain == 'foxnews.com'].url]) ## No election updates ##
    fox_election_index = df[df.domain == 'foxnews.com'].url.index.to_list()
    fox_election_dict = {fox_election_index[i]:fox_election_boolean[i] for i in range(len(fox_election_index))}
    ### Exclude CNN Data, Live News, and Video Pages ###
    cnn_boolean = [(url.split('/')[3]!= 'data') &
               (url.split('/')[3]!= 'videos')& 
               (url.split('/')[4]!= 'live-news') for url in df[df.domain == 'cnn.com'].url.to_list()] 
    cnn_index = df[df.domain == 'cnn.com'].url.index.to_list()
    cnn_dict = pd.Series({cnn_index[i]:cnn_boolean[i] for i in range(len(cnn_boolean))})
    df = df[cnn_dict|
            (df.url_host == 'edition.cnn.com')|
            (df.domain == 'cnbc.com')| ## include cnbc ##
            pd.Series(fox_election_dict)
           ]
    df = df[((abs(df.url_dir_page_subj)>0) | (abs(df.url_dir_page_pola)>0))] ### OR condition as per meeting ###
    return df 
df_filtered = filter_df(path) ### run filter on file name 
df_cnbc = df_filtered[df_filtered.domain == 'cnbc.com'] ### filter for cnbc
df_cnn = df_filtered[df_filtered.domain == 'cnn.com'] ### filter for cnn
df_fox = df_filtered[df_filtered.domain == 'foxnews.com'] ### filter for fox news
out_folder = '/project/mechums/misinfo/url_text_mining/filtered_data_4_14_2023'
df_cnbc.to_csv(out_folder + '/' + path.split('/')[6].split('.')[0] + '_cnbc_filtered.csv') ### export cnbc
df_cnn.to_csv(out_folder + '/' + path.split('/')[6].split('.')[0] + '_cnn_filtered.csv') ### export cnn
df_fox.to_csv(out_folder + '/' + path.split('/')[6].split('.')[0] + '_fox_filtered.csv') ### export fox
print(out_folder + '/' + path.split('/')[6].split('.')[0] + '_filtered.csv') ### print out file name in .out for validation