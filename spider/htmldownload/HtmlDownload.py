# -*- coding:utf-8 -*-

#date:03/06/2018
#author:neil yue
#function:
#
#
#
#
#notes:

import requests

class HtmlDownload(object):
    def __init__(self):
        pass

    def htmldownload(self, url):
        '''
        对于提供的url返回请求后的网页源码
        :param url: url
        :return: str格式的网页源码
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
        }

        if url is None:
            print('sorry the url provided is None')
            return

        #value1 = url[39:44]
        #value2 = url[46:]

        try:
            r = requests.session()
            r.keep_alive = False
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                html_text = response.text
                return html_text
            else:
                print("the requests failed")
        except:
            print('sorry htmldownload failed')

    def get_url_key(self, url):
        value1 = url[39:44]
        value2 = url[46:]

        return value1, value2