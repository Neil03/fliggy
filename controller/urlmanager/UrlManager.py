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
import pymysql
from redis import StrictRedis


class UrlManager(object):
    def __init__(self):
        self.urls = queue.Queue()

        db = pymysql.connect(host='localhost', user='root', password='47811510Yu3=', port=3306, db='spider')
        cursor = db.cursor()

        #redis = StrictRedis(host='localhost', port=6379)

        sql = "SELECT * FROM urls"

        try:
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                self.urls.put(row[3])
        except:
            print('Error')

    def has_new_url(self):
        return self.urls.qsize()

    def get_url(self):
        url = self.urls.get()
        return url