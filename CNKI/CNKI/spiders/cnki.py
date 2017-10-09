# Created by Landuy at 2017/10/9
import scrapy
from scrapy import Request
from urllib import parse
from CNKI.items import CnkiItem
import re


class cnkiSpider(scrapy.Spider):
    name = 'cnkisp'
    # allowed_domains = ["www.cnki.net"]
    start_urls = ["http://kns.cnki.net/kns/brief/result.aspx?dbPrefix=SCPD"]

    cookies = {
        "ASP.NET_SessionId": "5atsoskm5rxqkirzhct0vjdb",
        "cnkiUserKey": "dd6eca65-a22c-330b-d486-22684afbe7b2",
        "Ecp_ClientId": "1171009095901465355",
        "Ecp_IpLoginFail": "171009112.81.2.110",
        "SID_kns": "123122",
        "SID_kinfo": "125102",
        "SID_klogin": "125141",
        "SID_kredis": "125142",
        "RsPerPage": "20"
    }
    meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Cookie" : "Ecp_ClientId=1171009095901465355; Ecp_IpLoginFail=171009112.81.2.110; RsPerPage=50; cnkiUserKey=dd6eca65-a22c-330b-d486-22684afbe7b2; ASP.NET_SessionId=5atsoskm5rxqkirzhct0vjdb; SID_kns=123122; SID_kinfo=125102; SID_klogin=125141; SID_kredis=125142; SID_krsnew=125132",

    }

    def start_requests(self):
        start_url = "http://kns.cnki.net/kns/brief/brief.aspx?" \
                    "curpage=1&RecordsPerPage=50" \
                    "&QueryID=5" \
                    "&ID=&turnpage=1" \
                    "&tpagemode=L" \
                    "&dbPrefix=SCPD" \
                    "&Fields=" \
                    "&DisplayMode=listmode" \
                    "&PageName=ASP.brief_result_aspx#J_ORDER&"

        yield Request(url=start_url, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        """
        得到专利详情页链接列表
        :param response:
        :return:
        """

        urls_node = response.css("table.GridTableContent tr")
        for node in urls_node[1:]:
            patent_detail_url = "http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?dbcode=SCPD&dbname=SCPD2017&filename="
            patent_url = node.css("a.fz14::attr(href)").extract_first("")
           # / kns / detail / detail.aspx?QueryID = 5 & CurRec = 8 & dbcode = scpd & dbname = SCPD2014 & filename = CN103786360A
            match_re = re.match(".*filename=(\w+)", patent_url)
            if match_re:
                patent_detail_url = patent_detail_url + match_re.group(1)
            else:
                print("url错误")
                continue
            print("专利详情url：", patent_detail_url)
            yield Request(url=patent_detail_url, callback=self.parse_detail,
                          headers=self.headers, cookies=self.cookies, meta=self.meta)

        # 提取下一页交给scrapy下载
        next_url = response.css("div.TitleLeftCell a::attr(href)").extract()[-1]
        print("next url is :", parse.urljoin(response.url, next_url))
        yield Request(url=parse.urljoin(response.url, next_url),
                       callback=parse, headers=self.headers, cookies=self.cookies, meta=self.meta)


    def parse_detail(self, response):
        """
        详情提取
        :param response:
        :return:
        """
        print("详情页提取")
        node_list = response.css("table#box tr")
        node_1 = node_list[0].css("td::text").extract()
        application_no = node_1[1].replace(u'\xa0', u'')
        application_day = node_1[3].replace(u'\xa0', u'')
        node_2 = node_list[1].css("td::text").extract()
        publication_no = node_2[1].replace(u'\xa0', u'')
        publication_day = node_2[3].replace(u'\xa0', u'')
        node_3 = node_list[2].css("td::text").extract()
        publication_user = node_3[1].replace(u'\xa0', u'')
        publication_address = node_3[3].replace(u'\xa0', u'')
        node_4 = node_list[4].css("td::text").extract()
        patent_inventor = node_4[1].replace(u'\xa0', u'')
        node_5 = node_list[7].css("td::text").extract()
        patent_agent = node_5[1].replace(u'\xa0', u'')
        patent_agent_user = node_5[3].replace(u'\xa0', u'')
        node_6 = node_list[10].css("td::text").extract()
        patent_summary = node_6[1].replace(u'\xa0', u'')
        node_7 = node_list[11].css("td::text").extract()
        patent_main_item = node_7[1].replace(u'\xa0', u'')
        # main_cls_no =
        # patent_cls_np =
        # patent_title =
        item = CnkiItem()
        item['application_no'] = application_no
        item['application_day'] = application_day
        item['publication_no'] = publication_no
        item['publication_day'] = publication_day
        item['publication_user'] = publication_user
        item['publication_address'] = publication_address
        item['patent_inventor'] = patent_inventor
        item['patent_agent'] = patent_agent
        item['patent_agent_user'] = patent_agent_user
        item['patent_summary'] = patent_summary
        item['patent_main_item'] = patent_main_item
        yield item