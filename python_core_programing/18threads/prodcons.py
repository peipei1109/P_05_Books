# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''

from random import randint
from time import time, sleep
from Queue import Queue
from MyTread import MyThread

def writeQ(queue):
    print 'Producting object for Q...'
    queue.put('xxx',1)
    print 'size now',queue.qsize()
    
def readQ(queue):
    val = queue.get(1)
    print 'consumed object from Q... size now', \
        queue.qsize()
        
def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1,3))
def reader(queue,loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(2, 5)) 
funcs=[writer,reader]
nfuncs=range(len(funcs))


def main():
    nloops=randint(2,5)
    q=Queue(32)
    threads=[]
    for i in nfuncs:
        t=MyThread(funcs[i],(q,nloops),funcs[i].__name__)
        threads.append(t)
    for i in nfuncs:
        threads[i].start()
        
    for i in nfuncs:
        threads[i].join()
    print 'all DONE'
    

    
    

if __name__=="__main__":
    main()