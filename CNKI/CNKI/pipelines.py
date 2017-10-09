# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CnkiPipeline(object):
    colname = ['application_no', 'application_day', 'publication_no',
               'publication_day', 'publication_user', 'publication_address',
               'patent_inventor', 'patent_agent', 'patent_agent_user',
               'publication_address', 'patent_inventor', 'patent_agent',
               'patent_agent_user', 'patent_summary', 'patent_main_item']

    def open_spider(self, spider):
        # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
        self.file = open('cnki_patent_info.csv', 'w', newline='')
        # 启动csv的字典写入方法
        self.writer = csv.DictWriter(self.file, self.colname)
        # 写入字段名称作为首行
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()


    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
