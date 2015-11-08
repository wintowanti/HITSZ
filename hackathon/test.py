#!/usr/bin/env python
#coding=utf8


""" Simulate a user login to Sina Weibo with cookie.
You can use this method to visit any page that requires login.
"""


import urllib2
import re


cookie = 'YF-V5-G0=4955da6a9f369238c2a1bc4f70789871; _s_tentry=baike.baidu.com; Apache=6773642250336.707.1444623009782; SINAGLOBAL=6773642250336.707.1444623009782; ULV=1444623009829:1:1:1:6773642250336.707.1444623009782:; YF-Page-G0=33322e8e203d0599cedcc51042ddadde; YF-Ugrow-G0=169004153682ef91866609488943c77f; WBtopGlobal_register_version=cde4e46930babd9e; SUS=SID-3475795904-1446900193-GZ-p8qrn-da3640c520ba17d1d1d9adc3ffd7d8fc; SUE=es%3D880f47e254a5c182db458d0c5fe9da6e%26ev%3Dv1%26es2%3D2808453c97b939ceb5d04b8e4b162da6%26rs0%3DbPoc9DdAa2QFetq5QZVNInDM9LpOcgYS28lvJADufhrIBIKUANlR9zsICS8uVzj0fObtLu0gtfCYhMaEAXlZTNeegDBVVk0J%252FgLFP8XCDlMqvgudqpFsReeFCGl%252BCUp3MOYrTYxFgtguW%252Bxchh1MBc86scNx%252Bbh8WlAChZyISZU%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1446900193%26et%3D1446986593%26d%3Dc909%26i%3Dd8fc%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D17%26st%3D0%26uid%3D3475795904%26name%3Dwintowanti%2540163.com%26nick%3D%25E9%25A2%259C%25E7%2591%25B6_mahome%26fmp%3D%26lcp%3D; SUB=_2A257OYGxDeTxGeVK7FcW-SvFyziIHXVYTvR5rDV8PUNbvtBeLUugkW83gXupwK6ID00qrD9kRFxahZvhyg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFVcdB42xx6hV--Ri.b3xYz5JpX5KMt; SUHB=0u5RdzcdPSltGI; ALF=1478436182; SSOLoginState=1446900193; wvr=6; UOR=v.baidu.com,widget.weibo.com,www.baidu.com'  # get your cookie from Chrome or Firefox
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
    'cookie': cookie
}


def visit():
    url = "http://weibo.com/u/2299273207"
    req = urllib2.Request(url, headers=headers)
    text = urllib2.urlopen(req).read()
    from pyquery import PyQuery as pq
    d = pq(text)
    print text
    fs = open("html.txt","w")
    fs.write(text)
    fs.close()
    print len(d(".WB_feed"))
    
    #print text
    # print the title, check if you login to weibo sucessfully
    pat_title = re.compile('<title>(.+?)</title>')
    r = pat_title.search(text)
    if r:
        print r.group(1)


if __name__ == '__main__':
    visit()
