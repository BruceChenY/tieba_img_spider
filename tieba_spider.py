import sqlite3
import requests
import re
import os
import time

tieba_name=''
request_time_out=1
time_sleep=1

class Scheduler():
    '''
    调度器，对url管理
    '''
    
    def __init__(self):
        self.queue_readly=[]
        self.queue_already=[]

    def add_url(self,url):
        if (url not in self.queue_readly) and (url not in self.queue_already):
            self.queue_readly.append(url)

    def get_url(self):
        if len(self.queue_readly)>0:
            url=self.queue_readly.pop(0)
            self.queue_already.append(url)
            return url
        else:
            return None
    def len_readly(self):
        return len(self.queue_readly)
    def len_already(self):
        return len(self.queue_already)

# https://tieba.baidu.com/f?kw=nba
# https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn=50

img_name=0 
class Spider():
    def __init__(self):
        self.scheduler_page=Scheduler()
        self.scheduler_list=Scheduler()
        self.img_name=0 
        self.list_count=0
    def get_page_url(self):
        url='https://tieba.baidu.com/f?kw='+tieba_name
        res=requests.get(url,timeout=request_time_out)
        #res.encoding='utf-8'
        text=res.text
        m=re.search(r'href=.*pn=(\d+).*尾页',text)
        page_count=int(m.group(1))
        ran_page=range(0,page_count+1,50)
        
        base_url='https://tieba.baidu.com/f?kw='+tieba_name+'&ie=utf-8&pn='
        for i in ran_page:
            self.scheduler_page.add_url(base_url+str(i))
        print(tieba_name+'共'+str(len(ran_page))+'页','url已经获取完成')
        print('已获取帖子链接%5d'%0,end='')
            
    def get_list_url(self):
        while True:
            url=self.scheduler_page.get_url()
            if url is None or self.list_count>1:
                break
            self.list_count+=1
            time.sleep(time_sleep)
            try:
                res=requests.get(url,timeout=request_time_out)
            except:
                continue
            text=res.text
            li=re.findall(r'href=\"(/p/\d+)',text)
            base_url='https://tieba.baidu.com'
            for i in li:
               self.scheduler_list.add_url(base_url+i)
               print('\b'*5,end='')
               print('%5d'%self.scheduler_list.len_readly(),end='',flush=True)
        print() 
        print(tieba_name+'吧共'+str(self.scheduler_list.len_readly())+'贴','url已经获取完成')
        print('已下载图片%5d'%0,'剩余贴页面数量%5d'%self.scheduler_list.len_readly(),end='',flush=True)
           
    def get_img_url(self):
        while True:
            url=self.scheduler_list.get_url()
            if url is None:
                return
            time.sleep(time_sleep)
            try:
                res=requests.get(url,timeout=request_time_out)
            except:
                continue
            text=res.text
            if 'pn=' not in url:
                m=re.search(r'共<span class="red">(\d+)</span>页',text)
                page_count=int(m.group(1))
                if page_count>1:
                    for i in range(2,page_count+1):
                        self.scheduler_list.add_url(url+'?pn='+str(i))
            
            li_img_url=re.findall(r'<img class="BDE_Image" pic_type="0".*?src="(.*?jpg)"',text)
            for i in li_img_url:
                time.sleep(time_sleep)
                try:
                    res=requests.get(i,timeout=request_time_out)
                except:
                    continue
                f=open('./img/'+str(self.img_name)+'.jpg','wb')
                self.img_name+=1
                f.write(res.content)
                f.close()
                print('\b'*35,end='')
                print('已下载图片%5d'%self.img_name,'剩余贴页面数量%5d'%self.scheduler_list.len_readly(),end='',flush=True)
           
    def start_spider(self):
        self.get_page_url()
        self.get_list_url()
        self.get_img_url()
            

'''
数据库连接方法
'''
def sql_connect():
    conn=sqlite3.connect('./'+tieba_name+'.db')
    cur=conn.cursor()
    return conn,cur

if __name__=='__main__':
    tieba_name=input('请输入贴吧名：')
    if not os.path.exists('./img'):
        os.makedirs('./img')
        
    spider=Spider()
    spider.start_spider()
    
    
