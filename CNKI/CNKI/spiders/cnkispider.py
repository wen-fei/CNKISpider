# -*- coding: utf-8 -*-
import scrapy

from cnki.items import CnkiItem


class CnkispiderSpider(scrapy.Spider):

    name = "cnkispider"
    allowed_domains = ["dbpub.cnki.net/Grid2008/Dbpub/Brief.aspx?ID=SCPD&subBase=all"]
    #专利号按顺序排列
    start_urls = ['http://dbpub.cnki.net/Grid2008/Dbpub/Detail.aspx?DBName=SCPD2010&FileName=CN'+str(j)+'U&QueryID=4&CurRec=1' for j in range(203369100, 204050060)]

    def parse(self, response):

        name = response.css('td[width="832"]::text').extract_first()
        cnki = response.css('#box')
        all = cnki.css('td[bgcolor="#FFFFFF"]::text').extract()
        item = CnkiItem()
        item['name'] = name
        item['number'] = all[0]
        item['data'] = all[1]
        item['outnumber'] = all[2]
        item['outdata'] = all[3]
        item['sname'] = all[4]
        item['add'] = all[5]
        item['fname'] = all[7]
        item['dadd'] = all[11]
        item['dname'] = all[12]
        item['pnum'] = all[14]
        item['keyword'] = all[15]
        item['pages'] = all[17]
        item['typenum'] = all[18]
        yield item
        #for i in range(302697180,303060980):
         #   url = 'http://dbpub.cnki.net/Grid2008/Dbpub/Detail.aspx?DBName=SCPD2010&FileName=CN'+str(i)+'S&QueryID=4&CurRec=1'
          #  yield scrapy.Request(url=url, callback=self.parse)