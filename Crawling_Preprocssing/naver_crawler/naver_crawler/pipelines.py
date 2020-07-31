# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class NaverCrawlerPipeline:
    def __init__(self):
        self.csvwriter = csv.writer(open('naver.csv','w', encoding='utf-8'))
        self.csvwriter.writerow(['media','time','body'])
    def process_item(self, item, spider):
        row=[]
        row.append(item['media'])
        row.append(item['time'])
        row.append(item['body'])
        self.csvwriter.writerow(row)
        return item
