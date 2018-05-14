# -*- coding:utf-8 -*-

#date:03/06/2018
#author:neil yue
#function:
#
#
#
#
#notes:

import queue
from lxml import etree
from spider.htmldownload.HtmlDownload import HtmlDownload

class HtmlParsing(object):
    def __init__(self):
        pass

    def get_jiudian_url(self, html_par):
        '''
        获得飞猪主界面网页中的酒店连接
        :param html_par: 飞猪主页的源码
        :return: 酒店的url
        '''

        try:
            html = etree.HTML(html_par)
            # 解析飞猪主页的所有url
            total_urls = html.xpath('//ul/li[contains(@class, "subnav-item-1")]/a[contains(@class, "has-trans")]/@href')
            # 拼接成完整的url
            url_jiudian = 'https:' + total_urls[0]
            return url_jiudian
        except:
            print('the parsing to get url_jiudian failed!')

    def get_jiudian_url_city(self, html_par):
        '''
        解析酒店主页的源码获得推荐城市的名称和酒店URL对应的字典
        :param html_par: 酒店主页的源码
        :return: 推荐城市名称和酒店URL的字典
        '''

        try:
            html = etree.HTML(html_par)
            # 解析酒店主页源码获得推荐城市名称和代码
            value = html.xpath('//div[contains(@class, "recommend-domestic")]/div/div/div/a/@data-value')
            city = html.xpath('//div[contains(@class, "recommend-domestic")]/div/div/div/a/text()')
            url = html.xpath('//div[contains(@class, "recommend-domestic")]/div/div/div/a[@class="selected"]/@href')

            # 构造字典
            city_dic = {
            }

            # 构造相同部分的url
            url_common = 'https:' + url[0][:40]

            # 向字典中添加城市对应的url
            for i in range(len(value)):
                city_dic[city[i]] = url_common + value[i]

            return city_dic

        except:
            print('the parsing to get jiudian_url of different city failed!')

    def get_jiudian_url_pages(self, html_par):
        '''
        获取单一城市推荐酒店的分页对应的url
        :param html_par: 城市推荐酒店源码
        :return: 每页对应的url
        '''

        try:
            html = etree.HTML(html_par)
            # 解析单一城市酒店分页对应的url
            url_pages = html.xpath('//div[@class="seo-pagination"]/a/@href')
            # 拼接成完整url
            for i in range(len(url_pages)):
                url_pages[i] = 'https:' + url_pages[i]

            return url_pages
        except:
            print('parsing to get url_pages failed!')

    def get_jiudian_url_page(self, html_par):
        '''
        获取每页的推荐酒店的url
        :param html_par: 推荐的每页酒店的源码
        :return: 推荐的每页酒店的url
        '''

        try:
            html = etree.HTML(html_par)
            # 解析每页的酒店url
            url_page = html.xpath('//div/div/div/div/div/div/h5/a/@href')
            # 拼接成完整的url
            for i in range(len(url_page)):
                url_page[i] = 'https:' + url_page[i]

            return url_page
        except:
            print('parsing to get jiudian_url_page failed')

    def get_url(self, html_par):
        '''
        根据种子URL的网页源代码解析获得最终所需的所有URL
        :return:最后需要爬去的所有URL集合
        '''

        # 存放未爬去url集合
        urls_new = queue.Queue()
        # 获取酒店url
        url_jiudian = self.get_jiudian_url(html_par)
        # 获取htmldownload
        htmldownload = HtmlDownload()
        # 获取酒店主页的html文档
        html_text_jiudian_main = htmldownload.htmldownload(url_jiudian)
        # 获取不同城市的url的字典
        dict_city = self.get_jiudian_url_city(html_text_jiudian_main)
        # 取出不同城市的推荐酒店的url

        # 构建一个队列用于存放不同城市的URL
        queue_city = queue.Queue()
        # 获取不同城市的URL并存放到队列中
        for key in dict_city:
            queue_city.put(dict_city[key])

        # 第一层遍历所有的城市
        #while not queue_city.empty():
        for i in range(2):
            # 获取X城市的酒店的URL
            url_city = queue_city.get()
            # 获取X城市的推荐酒店主页的源码
            html_text_jiudian_city = htmldownload.htmldownload(url_city)
            # 获取X城市推荐酒店的分页的URL
            url_jiudian_pages = self.get_jiudian_url_pages(html_text_jiudian_city)

            # 第二层遍历遍历一个分页
            #for j in range(len(url_jiudian_pages)):
            for j in range(3):
                # 获取X城市的推荐酒店的Y页的URL
                url_jiudian_page = url_jiudian_pages[j]
                # 获取X城市的推荐酒店的Y页的网页源码
                html_text_jiudian_city_page = htmldownload.htmldownload(url_jiudian_page)
                # 获取X城市的推荐酒店的Y页的所有酒店的url
                url_jiudian_city_pages = self.get_jiudian_url_page(html_text_jiudian_city_page)

                # 第三层遍历获取X城市推荐酒店第Y页的第Z个酒店的URL
                #for k in range(len(url_jiudian_city_pages)):
                for k in range(4):
                    # 将获取的URL添加到集合中
                    urls_new.put(url_jiudian_city_pages[k])

        return urls_new

    def get_name(self, html_par):
        '''
        获取酒店的名字
        :param html_par:酒店主页源码
        :return: 酒店的名字
        '''

        try:
            html = etree.HTML(html_par)
            # 获取酒店名字
            name = html.xpath('//div[@class="hotel-page"]/div[@class="hotel-content"]/div[@class="hotel-crumbs"]/div[@class="crumbs"]/span/text()')
            # 返回酒店名字的字符串
            return name[0]
        except:
            print('parsing to get name failed')

    def get_comment(self, html_par):
        '''
        获取评论
        :param html_par:酒店源码
        :return: 酒店评论
        '''

        try:
            html = etree.HTML(html_par)
            # 获取酒店评论
            comment = html.xpath('//div[@class="tb-r-cnt"]/text()')

            return comment
        except:
            print('parsing to get comment failed')

    def get_data(self, html_par):
        '''
        获取酒店源代码返回酒店名和评论的字典
        :param html_par: 酒店源代码
        :return: 酒店名和评论的字典
        '''

        htmldownload = HtmlDownload()
        value_1, value_2 = htmldownload.get_url_key()
        try:
            key = value_1 + '_' + value_2
            comment = self.get_comment(html_par)

            data = {
                key:comment
            }

            return data
        except:
            print('parsing to get data failed!')

