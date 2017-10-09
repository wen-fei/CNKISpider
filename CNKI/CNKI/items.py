# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field


class CnkiItem(Item):
    application_no = Field()
    publication_no = Field()
    application_day = Field()
    publication_day = Field()
    publication_user = Field()
    publication_address = Field()
    patent_inventor = Field()
    patent_agent = Field()
    patent_agent_user = Field()
    patent_summary = Field()
    patent_main_item = Field()
    main_cls_no = Field()
    patent_cls_np = Field()
    patent_title = Field()
