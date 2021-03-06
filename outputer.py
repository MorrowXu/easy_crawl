#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Morrow
# @IDE     : PyCharm
# @File    : outputer.py
# @Email   : 464580843@qq.com
# Create on 2018/3/1 11:37
import pymysql as mysql
import time


class Outputer(object):
    """
    将解析好的data存入mysqldb
    """
    def __init__(self):
        self.db = mysql.connect(host = 'localhost', user = 'root', passwd = '930502', db = 'webcrawler', charset = 'utf8')
        self.cursor = self.db.cursor()

    def sql_cennector(self, data):
        # 连接mysql数据库
        sql = '''INSERT INTO baike_key(key_word, content, url) VALUES("%s","%s", "%s")'''\
                % (data['title'].strip(), data['summary'].strip().replace('"',"'"), data['url']) # replace""防止sql语法报错
        # print sql
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
            # print('Query OK!')
        except Exception as e:
            # 发生错误时回滚,打印错误日志
            t = time.strftime('%Y_%m_%d')
            with open('%s_log.txt' % t, 'a+') as f: # 'a+' 为追加模式
                f.write(time.ctime()+' >>> '+ 'failed'+ '\t' +data['url'] + '\t' + str(e))
                f.write('\n\n\n')
            print('Query failed: %s' % e)
            self.db.rollback()

    def log_connector(self, log_dict):
        sql = '''INSERT INTO log(log_time, log_status, url) VALUES("%s", "%d", "%s")''' \
              % (log_dict['log_time'], 1, log_dict['url']) # 抓取成功则执行此语句

        if log_dict['log_status'] == 'failed':
            sql = '''INSERT INTO log(log_time, log_status, url, failed_resaon) VALUES("%s", "%s", "%s", "%s")''' \
                  % (log_dict['log_time'], 0, log_dict['url'], log_dict['failed_reason']) # 抓取不成功则

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('日志错误: %s' % e)


    def sql_closer(self):
        self.db.close()
        print('mysql is already closed...')
        # pass
