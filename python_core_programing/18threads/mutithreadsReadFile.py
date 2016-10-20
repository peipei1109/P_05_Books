# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''

from random import randint
from time import ctime, sleep

import Queue
import threading

class MyTask(object):
    """具体的任务类"""
    def __init__(self,name):
        self.name=name
        self._work_time=randint(1,5)
    def work(self):
        print("Task %s is start : %s, sleep time= %d" % (self.name, ctime(), self._work_time))
        sleep(self._work_time)
        print("Task %s is end : %s" % (self.name, ctime()))

class MyThread(threading.Thread):
    """多线程的类"""
    def __init__(self, my_queue):
        super(MyThread, self).__init__()
        self.my_queue = my_queue
        
    def run(self):
        while True:
            if self.my_queue.qsize()>0:
                self.my_queue.get().work()
            else:
                break
    
def print_split_line(num=30):
    print ('*'*num)
            
if __name__=="__main__":
    print_split_line()
    
    import my_read_file
    
    #分割文件
    sf=my_read_file.SplitFiles(r"E:\workspace\04CorePython\multiple_thread_read_file.txt",20)
    file_num=sf.split_file()
    
    queue_length=file_num
    my_queue=Queue.LifoQueue(queue_length)
    threads=[]
    
    for i in range(queue_length):
        file_name=sf.get_part_file_name(i)
        mt=MyTask(file_name)
        my_queue.put_nowait(mt)
    
    for i in range(queue_length):
        mtd=MyThread(my_queue)
        threads.append(mtd)
    
    for i in range(queue_length):
        threads[i].start()
    
    for i in range(queue_length):
        threads[i].join()    
        
    print_split_line()    
    