# -*- coding:utf-8 -*-

#date:03/06/2018
#author:neil yue
#function:
#
#
#
#
#notes:

from spider.htmldownload.HtmlDownload import HtmlDownload
from spider.htmlparsing.HtmlParsing import HtmlParsing
from controller.datastore.DataStore import DataStore

if __name__=='__main__':

    htmldownload = HtmlDownload()
    htmlparsing = HtmlParsing()
    datastore = DataStore()

    seed = 'https://www.fliggy.com'

    html_text = htmldownload.htmldownload(seed)
    urls = htmlparsing.get_url(html_text)

    print(urls)
    print(urls.qsize())
    print(urls.qsize())
    for i in range(urls.qsize()):
        url = urls.get()
        value1 = url[39:44]
        print(type(value1))
        value2 = url[46:]
        print(type(value2))
        print(type(url))
        print(value1)
        print(value2)
        print(url)

        message = {
            'id': i,
            'city': value1,
            'special': value2,
            'url': url
        }

        datastore.urls_save(message)


