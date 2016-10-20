# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''
#多线程的资源同步，可使用thread.RLock()来创建资源锁，然后使用acquire()来锁住资源，release()来释放资源。
#待事件用thread.Event()，用wait()来等待事件，set()来激发事件，clear()用于清除已激发事件。


import time # 导入时间模块
import threading as thread # 导入线程模块
 
class Thread1(thread.Thread):
    def __init__(self):
        thread.Thread.__init__(self) # 默认初始化
        self.lock = thread.RLock() # 创建资源锁
        self.flag = True
        self.count = 0
    def run(self):
        print 'Thread1 run',time.ctime()
        while self.count < 3:
            self.lock.acquire() # 锁住资源
            self.count += 1
            print self.count # 输出计数
            self.lock.release() # 释放资源
            time.sleep(1) # 线程休眠1秒
        print 'Thread1 end',time.ctime()
        
class Thread2(thread.Thread):
    def __init__(self,event):
        thread.Thread.__init__(self) # 初始化线程
        self.event = event
    def run(self):
        self.event.wait() # 线程启动后等待事件
        print 'Thread2 run',time.ctime()
        self.event.clear() # 清除事件
        print 'Thread2 end',time.ctime()
 
print 'program start'
event = thread.Event()
t1 = Thread1()
t2 = Thread2(event)
t1.start() # 线程t1启动
t2.start() # 线程t2启动
event.set() # 激发事件t2开始运行 
t1.join() # 主线程挂起，等待线程t1结束
t2.join() # 主线程挂起，等待线程t2结束
print 'program end' # 结束程序
 