import sqlite3
import requests

tieba_name=''

class Scheduler():
    '''
    调度器，对url管理
    '''
    
    def __init__(self):
        self.queue_readly=[]
        self.queue_already=[]

    def add_url(self,url):
        if url not in self.queue_readly and url not in self.queue_already:
            self.queue_readly.append(url)

    def get_url(self):
        if len(self.queue_already)>0:
            url=self.queue_readly.pop(0)
            self.queue_already.append(url)
            return url
        else:
            return None

https://tieba.baidu.com/f?kw=nba
https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn=50


'''
数据库连接方法
'''
def sql_connect():
    conn=sqlite3.connect('./'+tieba_name+'.db')
    cur=conn.cursor()
    return conn,cur

if __name__=='__main__':
    tieba_name=input('请输入贴吧名：')
