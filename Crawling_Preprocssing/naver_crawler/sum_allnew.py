import pandas as pd
import re
import numpy as np
import csv
import glob
import pickle


path = '' #CSV 파일이 존재하는 경로 

file_list = glob.glob(path + '*.csv') #현재위치에 전처리된 csv파일
print(file_list)

for i, file in enumerate(file_list):
    if i==0:
        df=pd.read_csv(file)
    else : 
        df1=pd.read_csv(file)
        df = pd.concat([df,df1])
df = df[['time','body']]
# df = df.drop_duplicates(['body']) #중복값제거 여부
df = df.groupby('time').sum()

df.to_pickle('ALLNEWS.pkl')

