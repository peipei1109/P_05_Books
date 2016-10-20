# -*- encoding: utf-8 -*-
'''
Created on 2016年8月4日

@author: LuoPei
'''

#http://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=404289525&idx=2&sn=a2cf851777a56179598596fca53b5900&scene=4#wechat_redirect

from threading import Thread
import Queue
import time
 
class TaskQueue(Queue.Queue):
 
    def __init__(self, num_workers=1):
        Queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.start_workers()
 
    def add_task(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((task, args, kwargs))
 
    def start_workers(self):
        for i in range(self.num_workers):
            t = Thread(target=self.worker)
            t.daemon = True #表示这个线程不重要
            t.start()
 
    def worker(self):
        #这个true应该就是问题所在，因为这个没有退出条件~~所以主线程不会退出。
        while True:
            print self.qsize()
            tupl = self.get()## queue.get() blocks the current thread until an item is retrieved. 
            item, args, kwargs = self.get()
            item(*args, **kwargs)
        self.task_done() #override的Queue.Queue
 
def tests():
    def blokkah(*args, **kwargs):
        time.sleep(5)
        print "Blokkah mofo!"

    q = TaskQueue(num_workers=5)
    
#     def gradient_descent():
#     # the gradient descent code
#     queue.add_task(plotly.write, x=X, y=Y)

    for item in range(10):
         q.add_task(blokkah)

    q.join() # block until all tasks are done
    print "All done!"

if __name__ == "__main__":
    tests()