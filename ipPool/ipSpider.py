# Created by Landuy at 2017/9/29
import urllib.request as urllib2
from bs4 import BeautifulSoup
import csv



def check_ip(ip_port):
    """检测ip是否可用，只爬取可用的ip"""
    #Todo 是用Scrapy进行爬取的时候在使用之前也要先检测代理是否可用，或者采取判断机制，不可用的直接抛弃
    return True
    pass



# py3 读文件写入做了严格的区分，不要用wb模式，用w模式，另外注意加上newline，否则文件会每个一行多一个空行
with open("ip_free_pool.csv", "w", newline="") as csvfile:
    write = csv.writer(csvfile)
    # 先写入columns_name
    write.writerow(["ip", "port", "address", "speed", "contact_speed", "protocol_type"])
    for page in range(1, 500):
        """
            只获取前50页的IP数量，足够备用
            需要筛选出高质量的代理IP
        """
        url = 'http://www.xicidaili.com/nn/%s' % page
        user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        request = urllib2.Request(url)
        request.add_header("User-Agent", user_agent)
        # 得到网页内容
        content = urllib2.urlopen(request)
        # 对网页进行解析
        soup = BeautifulSoup(content, 'lxml')
        # 获取本页面所有的ip列表
        trs = soup.find('table', {"id": "ip_list"}).findAll('tr')
        # print(trs) # 测试有数据
        # 对ip进行提取，trs[0]是表头，过滤掉
        for tr in trs[1:]:
            tds = tr.findAll('td')
            # ip地址
            ip = tds[1].text.strip()
            # 端口
            port = tds[2].text.strip()
            # 类型
            protocol_type = tds[5].text.strip()
            # 服务器地址, 有可能为空
            address = tds[3].find('a')
            if address is None:
                address= "UNKNOW"
            else:
                address = address.text
            # 获取速度 attrs可以获取标签内的属性的内容，[:-1] 可以截断字符串弃掉非数字内容
            speed = tds[6].find('div').attrs['title'][:-1]
            # 筛选速度比较好的
            if float(speed) > 2:
                continue
            else:
                # 获取链接速度
                contact_speed = tds[7].find('div').attrs['title'][:-1]
                if float(contact_speed) > 2:
                    continue
                else:
                    # 检测代理是否可用
                    ip_port = ip + ":" + port
                    can_use = check_ip(ip_port)
                    if can_use is True:
                        # 写入多行用writerows
                        write.writerow([ip, port, address, speed, contact_speed, protocol_type])
                        print(ip, port, address, speed, contact_speed, protocol_type)
                    else:
                        print("代理不可用")
