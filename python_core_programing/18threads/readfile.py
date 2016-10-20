# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''
#https://segmentfault.com/q/1010000000413394
#把文件描述符当做临界资源

import threading
import time

mutex = threading.Lock()
fp = open(r'E:\workspace\04CorePython\test.txt')


class Reader(threading.Thread):
    def __init__(self, num):
        super(Reader,self).__init__()
        self.num = num

    def run(self):
        while True:
            with mutex:
                line = fp.readline()
                if len(line) == 0:
                    return
                print'%d:%s' % (self.num, line), time.ctime()
            time.sleep(0.1)


if __name__ == '__main__':
    r1 = Reader(1)
    r2 = Reader(2)
    r1.start()
    r2.start()

    r1.join()
    r2.join()


