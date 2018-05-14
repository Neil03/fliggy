# -*- coding:utf-8 -*-

#date:03/06/2018
#author:neil yue
#function:
#
#
#
#
#notes:

from multiprocessing.managers import BaseManager

from spider.htmldownload.HtmlDownload import HtmlDownload
from spider.htmlparsing.HtmlParsing import HtmlParsing

class Worker(object):
    def __init__(self):
        pass

    def worker(self):
        # 创建类似的QueueManager:
        class QueueManager(BaseManager):
            pass

        # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
        QueueManager.register('get_task_queue')
        QueueManager.register('get_result_queue')

        # 连接到服务器，也就是运行task_master.py的机器:
        server_addr = '59.69.10.23'
        print('Connect to server %s...' % server_addr)

        # 端口和验证码注意保持与task_master.py设置的完全一致:
        m = QueueManager(address=(server_addr, 5000), authkey=b'hello')

        # 从网络连接:
        m.connect()

        # 获取Queue的对象:
        task_queue = m.get_task_queue()
        result_queue = m.get_result_queue()

        return task_queue, result_queue

class Spider(object):
    def __init__(self):
        pass

    def crawl(self, url_queue, result_queue, htmldownload, htmlparsing):

        while True:
            if not url_queue.empty():
                url = url_queue.get(timeout=50)
                if url != 'end':
                    #print(url)
                    #print('爬虫节点获取url管理进程通过url_queue传过来的url')
                    html_text = htmldownload.htmldownload(url)
                    value_1, value_2 = htmldownload.get_url_key(url)
                    key = value_1 + '_' + value_2

                    comment = htmlparsing.get_comment(html_text)
                    data = {
                        key: comment
                    }
                    result_queue.put(data)
                    #print(comment)
                    #print('爬虫节点通过result_queue将评论数据传给数据提取进程')
                else:
                    result_queue.put('end')
                    return

if __name__=='__main__':
    worker = Worker()

    task_queue, result_queue = worker.worker()

    htmldownload = HtmlDownload()
    htmlparsing = HtmlParsing()

    spider = Spider()

    spider.crawl(task_queue, result_queue, htmldownload, htmlparsing)

    # 处理结束:
    print('worker exit.')