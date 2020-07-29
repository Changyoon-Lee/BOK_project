import pandas as pd
import re
import numpy as np
import csv
import glob
from tqdm import tqdm


df = pd.read_csv('연합뉴스전처리해야됨.csv', parse_dates=['time'])


def clean_text(text):
#     cleaned_text = re.findall('= (.+)\,[\\ \'\,a-z]+?@', text)
    cleaned_text = re.findall('= (.+)', text)
    if cleaned_text != []:
        cleaned_text = re.sub('[\\ \'\,a-zA-Z0-9]+?@.+','', cleaned_text[0])
        cleaned_text = re.sub('[▲■◆※\{\}\[\]\/?,;:|*~`!^\-_+<>@\#$%&\\\=\'\"]','', cleaned_text)
        cleaned_text = re.sub('r    ' , '', cleaned_text)
        cleaned_text = re.sub('  ', '', cleaned_text)

    elif len(re.findall('[가-힣]', text))<30:cleaned_text = []
        
    else :    
        cleaned_text = re.findall('([가-힣].+),.*\(끝', text)
        if cleaned_text !=[]:
            cleaned_text = re.sub('[◆■▲※\{\}\[\]\/?,;:|*~`!^\-_+<>@\#$%&\\\=\'r"]','', cleaned_text[0])
            cleaned_text = re.sub('r    ' , '', cleaned_text)
            cleaned_text = re.sub('  ', '', cleaned_text)
        else : 
            cleaned_text = re.findall('([가-힣].+)', text)
            cleaned_text = re.sub('[◆■▲※\{\}\[\]\/?,;:|*~`!^\-_+<>@\#$%&\\\=\'r"]','', cleaned_text[0])
            cleaned_text = re.sub('r    ' , '', cleaned_text)
            cleaned_text = re.sub('  ', '', cleaned_text)
    return cleaned_text
#73786개 ->73744 ->

idx_del = df[df['body'] == '[]'].index
df = df.drop(idx_del)
suma=[]

with open('연합뉴스전처리완', 'w', encoding='utf-8') as f:
    cn=0
    for i in tqdm(range(74)): #i*1000 ~ (i+1)*1000
        
        if i<73:
            a = [clean_text(val) for val in df['body'][i*1000:(i+1)*1000]]
            suma.extend(a)
        else :
            a = [clean_text(val) for val in df['body'][i*1000:]]
            suma.extend(a)

        # [clean_text(i) for i in df['body']]
    df['body'] = suma
    idx_del = df[df['body'] == '[]'].index
    df = df.drop(idx_del)

    df.to_csv(f,index=False, header=True, encoding='utf-8')
    print('전처리 완료')
