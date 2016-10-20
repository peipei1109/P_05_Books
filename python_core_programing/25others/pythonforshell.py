# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''

import subprocess
import multiprocessing
import os
import shlex
import sys



def run_cmd_wait_for_stop(cmd_str):
    p=subprocess.Popen(shlex.split(cmd_str),stdout=subprocess.PIPE,stderr=subprocess.PIPE )
    res,error=p.communicate()
    return res


if __name__=="__main__":
    res=run_cmd_wait_for_stop("ipconfig")
    print "中文",str(res)
    print sys.getdefaultencoding()