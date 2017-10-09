# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent

class CnkiSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def process_request(self, request, spider):
        # def get_ua():
            # return getattr(self.ua, self.ua_type)

        # random_agent = get_ua()
        # request.headers.setdefault("User-Agent", get_ua())
        # 设置代理
        # request.meta['proxy'] = ""
        request.headers.setdefault("Cookie", "Ecp_ClientId=2170914074501149831; RsPerPage=20; cnkiUserKey=42463fbc-f813-8023-21c7-d4cd29c7bff8; ASP.NET_SessionId=u3vqombtchoej45crc4daaue; SID_kns=123119; SID_kinfo=125104; SID_klogin=125144; SID_krsnew=125131; SID_kredis=125144; Ecp_IpLoginFail=171009112.81.2.110")