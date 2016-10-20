# -*- encoding: utf-8 -*-
'''
Created on 2016年8月4日

@author: LuoPei
'''



#在 Python 中有个两个库包含了 map 函数： multiprocessing 和它鲜为人知的子库 multiprocessing.dummy
#dummy 是 multiprocessing 模块的完整克隆，唯一的不同在于 multiprocessing 作用于进程，而 dummy 模块作用于线程（因此也包括了 Python 所有常见的多线程限制）。
#所以替换使用这两个库异常容易。你可以针对 IO 密集型任务和 CPU 密集型任务来选择不同的库。

import urllib2 
from multiprocessing.dummy import Pool as ThreadPool 
 
urls = [
    'http://www.python.org', 
    'http://www.python.org/about/',
    'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
    'http://www.python.org/getit/',
    'http://www.python.org/community/',
    'https://wiki.python.org/moin/',
    'http://planet.python.org/',
    'https://wiki.python.org/moin/LocalUserGroups',
    'http://www.python.org/psf/',
    'http://docs.python.org/devguide/',
    'http://www.python.org/community/awards/'
    # etc.. 
    ]
 
# Make the Pool of workers
pool = ThreadPool(4) 
# Open the urls in their own threads
# and return the results
results = pool.map(urllib2.urlopen, urls)
#close the pool and wait for the work to finish 
pool.close() 
pool.join() 