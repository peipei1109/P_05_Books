#!/usr/bin/env python
#--*-- coding:utf-8 --*--
#python 遍历修改工程下所有CVS/Root文件

#http://blog.csdn.net/zhang_red/article/details/9056899

import os

list_path = r"F:\IntelliJIDEA_workspace\maven\sgh_findgame"

#os.walk(path),遍历path，返回一个对象，他的每个部分都是一个三元组,('目录x'，[目录x下的目录list]，目录x下面的文件
def walk_dir(dir,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name == "Root":
                file_full_path = os.path.join(root,name)
                with open(file_full_path, "w") as file :
                    file.writelines(":pserver:myName@cvsHost:/data/cvsroot") 

        for name in dirs: # 这个在该功能中没啥用
            if name == "Root":
                file_full_path = os.path.join(root,name)
                with open(file_full_path) as file :
                    print(file.readlines())

walk_dir(list_path)