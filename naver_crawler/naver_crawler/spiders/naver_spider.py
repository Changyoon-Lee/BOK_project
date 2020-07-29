import scrapy
import re
from naver_crawler.items import NaverCrawlerItem
from datetime import datetime
from dateutil.relativedelta import  relativedelta
class NaverSpider(scrapy.Spider):
    name = "naver"
#사용시 수정해야할 사항 : 시작날짜, 마지막 날짜, 미디어 설정(cookie)
    def start_requests(self):
        date1 = 0
        date2 = 0
        time_start = datetime(2005,5,1) # 크롤링할 시작 날짜
        last_year = 2017
        #네이버 뉴스 페이지가 400이 한계-> 월별로 나눠서 검색하여 파싱한다
        while True: # 17년도 까지만 크롤링 할 예정

            if date1 != 0:
                date1 = date1 + relativedelta(months=1)
                date2 = date1 + relativedelta(months=1, days=-1)
                #날짜 format바꿈
                ds = datetime.strftime(date1,'%Y.%m.%d')
                de = datetime.strftime(date2,'%Y.%m.%d')
                
                #2006년 넘어가면 작업 중지
                if date1.year == last_year+1:
                    break
            else : 
                date1 = time_start
                date2 = date1 + relativedelta(months=1, days=-1)
                ds = datetime.strftime(date1,'%Y.%m.%d')
                de = datetime.strftime(date2,'%Y.%m.%d')


            url_org = 'https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=2&mynews=1&pd=3&ds={}&de={}'.format(ds, de)
            yield scrapy.Request(url=url_org, cookies={'news_office_checked': '2227'}, callback=self.parse_url_num)#,2227,1018,1001
            #request에 cookie 추가

    def parse_url_num(self, response):

        article_num=re.findall('\d+',response.xpath('//*[@id="main_pack"]/div[2]/div[1]/div[1]/span/text()').extract()[0].split(' ')[-1].replace(',',''))[0]
        print(article_num,'------------'*3)

        #마지막 페이지넘버계산
        max_page = (int(article_num)//10)*10+1
        # print(max_page,'-----------------')
        for i in range(1,max_page,10):
            
            url=response.url+'&start={}'.format(i)

            yield scrapy.Request(url=url, meta={'article_num':article_num, 'max_page':max_page}, callback=self.parse_url)
            
    def parse_url(self, response):

        for sel in response.xpath('//*[@id="main_pack"]/div/ul/li'):
           
            med = sel.xpath('//span[@class="_sp_each_source"]/text()').extract()[0]#media 어디인지 파싱한것

            if med=='연합뉴스'or med =='이데일리':   
                url=sel.xpath('dl/dd/a/@href').extract()[0]
                time=sel.xpath('dl/dd[1]/text()').getall()[1]//*[@id="sp_nws1"]/dl/dd[1]/text()
                print(time)
                yield scrapy.Request(url=url, callback=self.parse_body, meta={'med':med,'time':time})
            elif med=='연합인포맥스':
                url=sel.xpath('dl/dt/a/@href').extract()[0]
                time=sel.xpath('dl/dd[1]/text()').getall()[1]
                print(time)
                yield scrapy.Request(url=url, callback=self.parse_infomax, meta={'med':med, 'time':time})

    #연합뉴스, 이데일리 파싱하는 함수
    def parse_body(self, response):
        item = NaverCrawlerItem()

        item['time'] = response.meta['time']
        item['body'] = response.xpath('//*[@id="articleBodyContents"]/text()').getall()
        item['media'] = response.meta['med']
        yield item

    #연합인포맥스부분 파싱함수
    def parse_infomax(self, response):
        item = NaverCrawlerItem()
       
        item['time'] = response.meta['time']
        
        item['body'] = response.xpath('//*[@id="article-view-content-div"]/text()').getall()
        item['media'] = response.meta['med']
        yield item
    # def parse_body(self, response):
        
    #     item = NaverCrawlerItem()
    #     item['body'] = response.xpath('//*[@id="articleBodyContents"]/text()[1]').extract()[0]
    #     item['time'] = response.xpath('//*[@id="main_content"]/div[1]/div[3]/div/span/text()').extract()[0]
    #     item['title'] = response.xpath('//*[@id="articleTitle"]/text()').extract()[0]
    #     yield item

        # page = re.findall('start=(.*)',response.url)
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
            
        #     f.write(response.xpath())
        #self.log('Saved file')

