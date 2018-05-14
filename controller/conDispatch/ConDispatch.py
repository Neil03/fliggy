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
from multiprocessing.managers import BaseManager
import threading

from controller.urlmanager.UrlManager import UrlManager
from controller.datastore.DataStore import DataStore

class Master(object):
    def __init__(self):
        pass

    def master(self, task_queue, result_queue):

        # 从BaseManager继承的QueueManager:
        class QueueManager(BaseManager):
            pass

        # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)

        # 绑定端口5000, 设置验证码'hello':
        manager = QueueManager(address=('100.87.44.79', 5000), authkey=b'hello')

        # 启动Queue:
        manager.start()

        # 获得通过网络访问的Queue对象:
        task_queue = manager.get_task_queue()
        result_queue = manager.get_result_queue()

        return task_queue, result_queue

class UrlManager_Thread(threading.Thread):
    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    def run(self):
        #print('url管理进程启动')
        # 获取urlmanager对象
        urlmanager = UrlManager()

        while (urlmanager.has_new_url()):
            # 取出一个未爬去的url
            url = urlmanager.get_url()
            #threadLock.acquire()
            # 将这个url发送给爬虫节点
            self.url_queue.put(url)
            #print('url由url管理进程发送给爬虫节点')
            #threadLock.release()
        else:
            self.url_queue.put('end')

class DataExact_Thread(threading.Thread):
    def __init__(self, result_queue, store_queue):
        threading.Thread.__init__(self)
        self.result_queue = result_queue
        self.store_queue = store_queue

    def run(self):

        while True:
            #threadLock.acquire()
            comment = self.result_queue.get(timeout=50)

            if comment != 'end':
                #print(comment)
                #print('数据提取进程获得由爬虫节点通过result_queue传过来的评论')
                #threadLock.release

                #threadLock.acquire
                self.store_queue.put(comment)
                #print('数据提取进程通过store_queue将评论数据传给数据存储进程')
                #threadLock.release
            else:
                self.store_queue.put('end')
                return

class DataStore_Thread(threading.Thread):
    def __init__(self, store_queue):
        threading.Thread.__init__(self)
        self.store_queue = store_queue

    def run(self):
        datastore = DataStore()

        while True:
            #threadLock.acquire()
            data = self.store_queue.get(timeout=50)
            if data != 'end':
                #print(data)
                #print('数据存储进程获得数据提取进程通过store_queeu传来的评论')
                #threadLock.release()
                datastore.comment_save(data)
            else:
                return


if __name__=='__main__':

    task_queue = queue.Queue()
    result_queue = queue.Queue()

    store_queue = queue.Queue()

    master = Master()

    task_queue, result_queue = master.master(task_queue, result_queue)

    # 创建url管理进程
    url_manager_thread = UrlManager_Thread(task_queue)
    # 创建数据提取进程
    data_exact_thread = DataExact_Thread(result_queue, store_queue)
    # 创建数据存储进程
    data_store_thread = DataStore_Thread(store_queue)

    threadLock = threading.Lock()
    threads = []

    # 启动三个进程
    url_manager_thread.start()
    data_exact_thread.start()
    data_store_thread.start()

    threads.append(url_manager_thread)
    threads.append(data_exact_thread)
    threads.append(data_store_thread)

    for thread in threads:
        thread.join()

