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

    
class Spider():
    def __init__(self):
        self.scheduler_page=Scheduler()
        self.scheduler_list=Scheduler()
    def get_page_url(self,tieba_name):
        url='https://tieba.baidu.com/f?kw='+tieba_name
        res=requests.get(url)
        #res.encoding='utf-8'
        text=res.text
        m=re.search(r'href=.*pn=(\d+).*尾页',text)
        page_count=int(m.group(1))
        ran_page=range(0,page_count+1,50)
        
        base_url='https://tieba.baidu.com/f?kw='+tieba_name+'&ie=utf-8&pn='
        for i in ran_page:
            slef.scheduler_page.add_url(base_url+str(i))
            
        
        

'''
数据库连接方法
'''
def sql_connect():
    conn=sqlite3.connect('./'+tieba_name+'.db')
    cur=conn.cursor()
    return conn,cur

if __name__=='__main__':
    tieba_name=input('请输入贴吧名：')
