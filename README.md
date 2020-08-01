# mulcamB_1조_BOK 의사록 논문구현
> Deciphering Monetary Policy Board Minutes through Text Mining Approach: The Case of 

> 진행순서:
> 데이터크롤링 -> 전처리 -> word porarity 계산 -> MPB tone계산 -> 기준금리와의 corr계산 및 시각화 -> pram변경하며 grid search


## 코드파일 설명
> Crawling_Preprocessing/naver_crawler\n
> /naver_crawler/spiders/naver_spider.py :네이버 뉴스 '금리'검색하여 연합뉴스,연합인포맥스, 이데일리 3사의 뉴스를 크롤링\n
> /preprocessing_edaily.py, ~infomax.py, ~yunhabnew.py 에서 각 뉴스사별 기사 전처리\n
> /sum_allnew.py 에서 전처리 된 파일 concat 후 time으로 groupby함



### 채권 데이터 추출.ipynb 
 1. 채권 보고서 데이터 수집
 - Beautiful Soup를 이용해 네이버 증권사 홈페이지에서 채권보고서 관련 정보(제목, 증권사, 날짜)와 다운로드용 url 크롤링
 - query 부분을 수정하여 데이터 수집 날짜를 지정할 수 있다.
 - 해당 보고서의 다운로드용 url을 request하여 원하는 날짜의 pdf파일을 다운로드할 수 있다.

 2. Tika parser를 이용해 다운로드한 PDF를 텍스트로 변환
 - pdfminer와 tika 양쪽 모두를 사용해 변환한 결과, tika가 더 높은 인식률을 보였다.
  > pdfminer가 인식하지 못해 생략한 문장을 tika를 통해 추출한 결과에선 찾아볼 수 있었다.
  > 이외에도, pdfminer를 사용한 텍스트 변환보다 tika를 사용한 텍스트 변환이 더 빠른 복도를 보였다.
 - tika parser를 이용해 다운로드한 pdf파일의 텍스트를 가져올 수 있다.


### 한국은행_의사록_코드_정리.ipynb
- 한국은행 의사록 데이터 수집 및 정제
1. crawling을 이용해서 한국은행 pdf_url을 가져오는 코드 작성
- .attrs[' ']를 이용하여 여러가지 리스트 중 원하는 .pdf파일만 가져올 수 있다.

2. tika, fitz parser를 이용해서 pdf to txt로 변환(총 145개의 의사록)
- 처음 'tika'를 활용하여 데이터를 가져왔을 경우 2006년~2007년 데이터에서 글자가 삭제되는 현상이 발생하였다. 그리하여 온전하게 모든 데이터를 담아 올 수 없게 되며 데이터 결측이 일어나게 된다.
총 145개의 sec2,sec3의 리스트 중에 121개만 가져오게 된다.(즉, 2006,2007년 데이터가 비게된다)
- 2006~2007년은 fitz를 활용해서 pdf to txt로 변환시켜주게 된다. 그러나 2006년 초반 data 몇개가 변환시
모든 글자가 깨지는 현상이 일어나게 된다. (ex. sec2는 정규표현식(?외환.?국제금융\s?동향.?과...)을 통해 내용을 정제하고 가져오는데 이때 '금'이라는 단어가 빠지면서 가져오지 못하는 현상이 발생한다. 

3. 각 부분의 현상들을 해결하기 위해 두개의 parser를 함께 사용하게 되었으며, 대부분 tika에 대해서 알고 있을 것 같아서 tika 보다는 fitz의 코드를 ppt에 넣어 내용 공유를 해주면 좋을 것 같아요..(개인적 생각)...

4. 데이터를 정제하고 pdf파일을 가져오는 것은 의사록 data를 만들어주신 분의 함수(강사님이 주신)를 사용했고 수정하지 않고 return 값으로 sec2,sec3의 데이터만 가져왔다.

5. 의사록 날짜 데이터는 crawling을 이용해서 가져왔다....(그리 중요하지는 않은 것 같아요...ㅎㅎ) 

6.pd.DataFtame을 통해 date,sec2,sec3의 데이터를 concat하였으며 결측지 데이터를 삭제 한 후에 sec2,sec3의 데이터를 하나로 합쳐준다.

7. data를 수집하고 정제하는 과정에서 대락적인 개요만 설명했고 자세한 것들을 코드에 주석처리 해 두었습니다. 의사록 데이터는 crawling과정이 어렵지는 않기 때문에(저는 삽질을 많이 했지만...) 데이터의 수집 과정만 짧게 설명하고 코드는 fitz정도만 소개해주어도 좋을 것 같습니다.ㅎㅎ



### CALLRATE.ipynb : 콜금리 크롤링

### 기준금리_전체기간.ipynb : 기준금리 크롤링 및 없는 날짜 이전값으로 채우기


### Pipeline 

ngramize --> 콜금리와merge --> word polarity 계산--> sent_tone, doc_tone계산 --> tone과 기준금리 비교시각화, corr계산

