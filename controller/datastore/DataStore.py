# -*- coding:utf-8 -*-

#date:03/06/2018
#author:neil yue
#function:
#
#
#
#
#notes:

import pymysql

class DataStore(object):
    def __init__(self):
        pass

    def comment_save(self, data):
        #print(data)
        #print(type(data))

        filename, = data
        comment, = data.values()

        try:
            with open(filename, 'wb') as file:
                for single_comment in comment:
                    file.write(str.encode(single_comment + '\n'))

        except:
            print('评论写文件失败')


    def urls_save(self, url):
        db = pymysql.connect(host='localhost', user='root', password='47811510Yu3=', port=3306, db='spider')
        cursor = db.cursor()

        table = 'urls'
        keys = ', '.join(url.keys())
        values = ', '.join(['%s'] * len(url))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                             values=values)
        update = ','.join([" {key} = %s".format(key=key) for key in url])
        sql += update
        try:
            if cursor.execute(sql, tuple(url.values()) * 2):
                print('Successful')
                db.commit()
        except:
            print('Failed')
            db.rollback()
        db.close()
