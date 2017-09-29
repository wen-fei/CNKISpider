# Created by Landuy at 2017/9/29
import urllib.request as urllib2
import threading

inFile = open('ip_free_pool.csv', 'r')
outFile = open('available.csv', 'w')
url = 'http://www.huangshanben.com/'
lock = threading.Lock()


def test():
    lock.acquire()
    line = inFile.readline().strip(',')[1:]
    lock.release()
    protocol, proxy = line[1], line[0]
    cookie = "PHPSESSID=5f7mbqghvk1kt5n9illa0nr175; kmsign=56023b6880039; KMUID=ezsEg1YCOzxg97EwAwUXAg=="
    try:
        proxy_support = urllib2.ProxyHandler({protocol.lower(): '://'.join(line.split('='))})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        request.add_header("cookie", cookie)
        content = urllib2.urlopen(request, timeout=4).read()
        if len(content) >= 1000:
            lock.acquire()
            print('add proxy', proxy)
            outFile.write('\"%s\",\n' % proxy)
            lock.release()
        else:
            print('出现验证码或IP被封杀')
    except Exception:
        print(Exception)


all_thread = []
for i in range(500):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()

for t in all_thread:
    t.join()

inFile.close()
outFile.close()