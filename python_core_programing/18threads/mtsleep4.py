# -*- encoding: utf-8 -*-
'''
Created on 2016年5月13日

@author: LuoPei
'''
import threading
from time import sleep,ctime



loops = [ 4, 2 ]

class threadFunc(object):
    def __init__(self,func, args, name=""):
        self.func=func
        self.args=args
        self.name=name
    
    def __call__(self):
        apply(self.func,self.args)
        
    
def loop(nloop, nsec):
    print 'start loop', nloop, 'at:', ctime()
    sleep(nsec)
    print 'loop', nloop, 'done at:', ctime()
    
def main():
    print "start at:", ctime()
    threads=[]
    nloops=range(len(loops))
    for i in nloops:
        t=threading.Thread(target=threadFunc(loop,(i,loops[i]),loop.__name__))
        threads.append(t)
        
    for i in nloops:
        threads[i].start()
    
    for i in nloops:
        threads[i].join()
    
    print 'all DONE at:',ctime()    
        

if __name__=="__main__":
    main()