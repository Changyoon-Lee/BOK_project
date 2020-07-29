###인포맥스 크롤링파일들 전처리 후 합치는 프로그램 입니다
import pandas as pd
import re
import numpy as np
import csv
import glob


def clean_text(text):
    cleaned_text = re.findall('= (.+)\(끝', text)
    if cleaned_text != []:
        cleaned_text = re.sub('[\\ \'\,a-zA-Z0-9]+?@.+','', cleaned_text[0])
        cleaned_text = re.sub('<.+>' , '', cleaned_text)
        cleaned_text = re.sub('[ㅇ▲※\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', cleaned_text)
    else:        
        cleaned_text = re.findall(' (.+),.*\(끝', text)
        if cleaned_text != []:
            cleaned_text = re.sub('<.+>' ,'', cleaned_text[0])
            cleaned_text = re.sub('[\\ \'\,a-zA-Z0-9]+?@.+','', cleaned_text)
            cleaned_text = re.sub('ㅇ▲※\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','', cleaned_text)
            cleaned_text = re.sub('(xa(.+)xa)','',cleaned_text)
            if len(re.findall('[가-힣]', cleaned_text))<30:
                cleaned_text = ''
        else : cleaned_text = ''
    return cleaned_text


path = 'csvfile/' #CSV 파일이 존재하는 경로 
merge_path = 'infomax_merge.csv' #최종 Merge file

file_list = glob.glob(path + '*')
print(file_list)

with open(merge_path, 'w', encoding='utf-8') as f:
    cn=0
    for file in file_list:
        cn+=1

        df = pd.read_csv(file, parse_dates=['time'])

        df['body'] = [clean_text(i) for i in df['body']]
        ###### 전처리
        idx_del = df[df['body'] == ''].index
        df = df.drop(idx_del)
        ###### 빈리스트 제거

        df=df[['media','time','body']]
        if cn==1:#첫번째에만 header를 넣었다
            df.to_csv(f,index=False, header=True, encoding='utf-8')
        else : 
            df.to_csv(f,index=False, header=False, encoding='utf-8')

        print('ok')

print('all ok')
