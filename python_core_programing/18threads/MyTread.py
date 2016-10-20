# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''
import threading
from time import ctime,sleep

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        print 'starting', self.name, 'at:', \
        ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished at:', \
        ctime()

    def getResult(self):
        return self.res
if __name__=="__main__":
    pass