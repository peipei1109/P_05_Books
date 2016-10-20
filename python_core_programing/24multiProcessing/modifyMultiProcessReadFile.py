# -*- encoding: utf-8 -*-
'''
Created on 2016年8月4日

@author: LuoPei
'''



# -*- coding: utf-8 -*-
 
import urlparse
import datetime
import os
from multiprocessing import Process,Queue,Array,RLock
 
WORKERS = 6
BLOCK_SIZE = 0
FILE_SIZE = 0
FILE_NAME = 'try.log'
 
def getFilesize(file):
    global FILE_SIZE
    fs = open(file,'r')
    fs.seek(0,os.SEEK_END)
    FILE_SIZE = fs.tell()
    fs.close()
 
def process_found(pid,array,rlock):
    global FILE_SIZE,BLOCK_SIZE
    fs = open(FILE_NAME,'rb')
    try:
        rlock.acquire()
        begin = array[0]
        end = (begin + BLOCK_SIZE)
        print begin,end
        if begin >= FILE_SIZE:
            print 'begin',begin
            array[0] = begin
            raise Exception('end of file')
        if end < FILE_SIZE:
            fs.seek(end)
            fs.readline()
            end = fs.tell()
        if end >= FILE_SIZE:
            end = FILE_SIZE
        array[0] = end
        print '-------------',begin,end
    except Exception, e:
        print e.__class__.__name__,str(e)
        return
    finally:
        rlock.release()
 
    fs.seek(begin)
    pos = begin
    fd = open('tmp_pid'+str(pid)+'_jobs','wb')
    while pos < end:
        fd.write(fs.readline())
        pos = fs.tell()
 
    fs.close()
    fd.close()
 
def main():
    global FILE_SIZE,BLOCK_SIZE,WORKERS,FILE_NAME
    getFilesize(FILE_NAME)
    BLOCK_SIZE = FILE_SIZE/WORKERS
    print FILE_SIZE,BLOCK_SIZE
    rlock = RLock()
    array = Array('l',WORKERS)
    array[0] = 0
    process=[]
    for i in range(WORKERS):
        p=Process(target=process_found, args=[i,array,rlock])
        process.append(p)
    for i in range(WORKERS):
        process[i].start()
    for i in range(WORKERS):
        process[i].join()
 
if __name__ == '__main__':
    main()