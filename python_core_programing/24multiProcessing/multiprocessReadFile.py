# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''
#print datetime.datetime.now().strftime("%Y/%d/%m %H:%M:%S")
#http://www.oschina.net/code/snippet_97079_4465

import urlparse
import datetime
import os
from multiprocessing import Process, Queue, Array, RLock
"""
多进程分块读取文件
"""

WORKERS = 4
BLOCKSIZE = 30
global FILE_SIZE

def getFilesize(file):
    """
        获取要读取文件的大小
    """
    global FILE_SIZE
    fstream = open(file,'r')
    fstream.seek(0,os.SEEK_END)
    FILE_SIZE = fstream.tell()
    fstream.close()

def process_found(pid, array, file, rlock,FILE_SIZE):
    #global FILE_SIZE
    global JOB
    global PREFIX
    """
        进程处理
        Args:
            pid:进程编号
            array:进程间共享队列，用于标记各进程所读的文件块结束位置
            file:所读文件名称
        各个进程先从array中获取当前最大的值为起始位置startpossition
        结束的位置endpossition (startpossition+BLOCKSIZE) if (startpossition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
        if startpossition==FILE_SIZE则进程结束
        if startpossition==0则从0开始读取
        if startpossition!=0为防止行被block截断的情况，先读一行不处理，从下一行开始正式处理
        if 当前位置 <=endpossition 就readline
        否则越过边界，就从新查找array中的最大值
    """
    fstream=open(file,'r')
    while True:
        rlock.acquire()
        print 'pid %s'% pid,','.join([str(v) for v in array])
        startposition=max(array)
        endposition=array[pid]=(startposition+BLOCKSIZE) if (startposition+BLOCKSIZE)<FILE_SIZE else FILE_SIZE
        rlock.release()
        print "startposition",startposition
        print "file_size",FILE_SIZE
        if startposition==FILE_SIZE: #END OF THIS FILE
            print 'pid%s end' %(pid)
            break
        
        elif startposition !=0:
            fstream.seek(startposition) #如果刚好在一行的最后隔断，就会少了一行，修改版本在modifyMultiProcessReadFile
            fstream.readline()
        pos=ss=fstream.tell()
        ostream = open('tmp_pid'+str(pid)+'_jobs'+str(endposition),'w')
        print  'tmp_pid'+str(pid)+'_jobs'+str(endposition)
        while pos<endposition:
            #处理line
            line=fstream.readline()
            ostream.write(line)
            pos=fstream.tell()
            
        print 'pid:%s,startposition:%s,endposition:%s,pos:%s'%(pid,ss,pos,pos)
        
        ostream.flush()
        ostream.close()
        ee=fstream.tell()
    fstream.close()     

def main():
    global FILE_SIZE
    print datetime.datetime.now().strftime("%Y/%d/%m %H:%M:%S") 
     
    file = r"E:\workspace\04CorePython\multiple_thread_read_file.txt"
    getFilesize(file)
    print "file size",FILE_SIZE
    
    rlock=RLock()
    array=Array('l',WORKERS,lock=rlock) 
    threads=[]
    for i in range(WORKERS):
        p=Process(target=process_found,args=[i,array,file,rlock,FILE_SIZE])
        threads.append(p)
    for i in range(WORKERS):
        threads[i].start()
    
    for i in range(WORKERS):
        threads[i].join()
    print datetime.datetime.now().strftime("%Y/%d/%m %H:%M:%S")    
           

if __name__=="__main__":
    main()