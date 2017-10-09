# Created by Landuy at 2017/10/9
import scrapy
import re
from scrapy import Request
from time import sleep
from urllib import parse
import requests

class cnkiSpider(scrapy.Spider):
    name = 'cnkisp'
    allowed_domains = ["http://www.cnki.net"]
    start_urls = ["http://kns.cnki.net/kns/brief/result.aspx?dbPrefix=SCPD"]


    def start_requests(self):
        start_url = "http://kns.cnki.net/kns/brief/brief.aspx?curpage=3&RecordsPerPage=50&QueryID=0&ID=&turnpage=1&tpagemode=L&dbPrefix=SCPD&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx#J_ORDER&"
        params = {
            # "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0",
            # "ConfigFile" : "SCPD.xml",
            # "DbCatalog" : "中国专利数据库",
            # "DbPrefix" : "SCPD",
            # "NaviCode" : "*",
            # "PageName" : "ASP.brief_result_aspx",
            # "action" : "",
            # "db_opt" : "SCPD",
            # "db_value" : "中国专利数据库",
            # "his" : "0",
            # "publishdate_from" : "2014-01-01",
            # "publishdate_to" : "2014-12-01",
            "pagename":	"ASP.brief_result_aspx",
            "dbPrefix":	"SCPD",
            "ConfigFile":"SCPD.xml",
            "dbCatalog" : "中国专利数据库",
            "research" :"off",
            "t" : "1507515739351",
            "keyValue":"",
            "S":"1"

        }
        cookies = {
            "ASP.NET_SessionId" : "5atsoskm5rxqkirzhct0vjdb",
            "cnkiUserKey":    "dd6eca65-a22c-330b-d486-22684afbe7b2",
            "Ecp_ClientId" : "1171009095901465355",
            "Ecp_IpLoginFail" : "171009112.81.2.110",
            "SID_kns":"123122",
            "SID_kinfo":"125102",
            "SID_klogin":"125141",
            "SID_kredis" : "125142",
            "RsPerPage" :"20"
        }
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Cookie" : "Ecp_ClientId=1171009095901465355; Ecp_IpLoginFail=171009112.81.2.110; RsPerPage=50; cnkiUserKey=dd6eca65-a22c-330b-d486-22684afbe7b2; ASP.NET_SessionId=5atsoskm5rxqkirzhct0vjdb; SID_kns=123122; SID_kinfo=125102; SID_klogin=125141; SID_kredis=125142; SID_krsnew=125132",

        }
        # request = requests.get(url=start_url, params = params, headers= headers)
        yield Request(url=start_url, headers=headers, cookies = cookies)


    def parse(self, response):
        """
        得到专利详情页链接列表
        :param response:
        :return:
        """
        urls_node = response.css(".GridTableContent tbody tr")
        for node in urls_node:
            patent_url = node.css("a.fz14::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, patent_url), callback=self.parse_detail)

        # 提取下一页交给scrapy下载
        next_url = response.css("div.TitleLeftCell a::attr(href)").extract()[-1]

    def parse_detail(self, response):
        pass
