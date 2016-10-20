# -*- encoding: utf-8 -*-
'''
Created on 2016年5月14日

@author: LuoPei
'''
'''
os.sep是获取系统默认文件路径分割符

os.walk(path),遍历path，返回一个对象，他的每个部分都是一个三元组,('目录x'，[目录x下的目录list]，目录x下面的文件

os.path.exists(part_file_name)
os.makedirs(part_file_name)

1.mkdir( path [,mode] )
      作用：创建一个目录，可以是相对或者绝对路径，mode的默认模式是0777。
      如果目录有多级，则创建最后一级。如果最后一级目录的上级目录有不存在的，则会抛出一个OSError，例如：
      
2.makedirs( path [,mode] )
      作用： 创建递归的目录树，可以是相对或者绝对路径，mode的默认模式也是0777。
      如果子目录创建失败或者已经存在，会抛出一个OSError的异常，Windows上Error 183即为目录已经存在的异常错误。如果path只有一级，与mkdir一样。例如：
'''
import os

class SplitFiles():
    """按行分割文件"""
    def __init__(self, file_name,line_count=200):
        """初始化呀分割的源文件名和分割后的文件行数"""
        self.file_name=file_name
        self.line_count=line_count
        
    def split_file(self):
        if self.file_name and os.path.exists(self.file_name):
            try:
                with open(self.file_name) as f: #使用with读文件
                    temp_count=0
                    temp_content=[]
                    part_num=1
                    for line in f:
                        if temp_count<self.line_count:
                            temp_count+=1
                        else:
                            self.write_file(part_num, temp_content)
                            part_num+=1
                            temp_count =1
                            temp_content=[]
                        temp_content.append(line)
                    else: #正常结束循环后将剩余的内容写入新文件中
                        self.write_file(part_num,temp_content)
                            
            except IOError as err:
                print err
            return part_num
        else:
            print("%s is not a validate file " % self.file_name)
            return 0
    
    def get_part_file_name(self, part_num):
        """"获取分割后的文件名称：在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
        temp_path=os.path.dirname(self.file_name)#获取文件的路径（不包含文件名）
        print temp_path
        part_file_name =temp_path+os.sep+"temp_part_file" 
        if not os.path.exists(part_file_name):
            os.makedirs(part_file_name)
        part_file_name +=os.sep+"temp_file"+str(part_num)+".part"
        return part_file_name
    
    def write_file(self,part_num, *line_content):
        """将按行分割后的内容写入相应的分割文件中"""
        part_file_name=self.get_part_file_name(part_num)
        print part_file_name
        print line_content
        try:
            with open(part_file_name,"w") as part_file:
                part_file.writelines(line_content[0])
        except IOError as err:
            print "nug",err        


if __name__=="__main__":
    sf = SplitFiles(r"E:\workspace\04CorePython\multiple_thread_read_file.txt",20)
    file_num=sf.split_file()
    print file_num