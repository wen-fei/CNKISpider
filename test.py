# Created by Landuy at 2017/9/29
import urllib.request as urllib2
from bs4 import BeautifulSoup
test_str = """
<td class="country"><img alt="Cn" src="http://fs.xicidaili.com/images/flag/cn.png"/></td>
<td>117.78.37.198</td>
<td>8000</td>
<td>
<a href="/2017-07-31/liaoning">辽宁鞍山</a>
</td>
<td class="country">高匿</td>
<td>HTTP</td>
<td class="country">
<div class="bar" title="0.032秒">
<div class="bar_inner fast" style="width:85%">
</div>
</div>
</td>
<td class="country">
<div class="bar" title="0.006秒">
<div class="bar_inner fast" style="width:98%">
</div>
</div>
</td>
<td>59天</td>
<td>17-09-29 13:31</td>
"""
soup = BeautifulSoup(test_str, 'lxml')
tds = soup.findAll('td')
for td in tds[1:]:
#     print(td)
    address = tds[3].find('a').text
    # 获取速度 attrs可以获取标签内的属性的内容，[:-1] 可以截断字符串弃掉非数字内容
    # speed = tds[5].find('div')
    speed = tds[6].find('div').attrs['title'][:-1]
    # 获取链接速度
    contact_speed = tds[7].find('div').attrs['title'][:-1]
    print(address)
    print(speed)
    print(contact_speed)

