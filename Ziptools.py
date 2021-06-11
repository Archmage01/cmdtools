#!/usr/bin/env python
# -*- coding:utf-8 -*-

import  zipfile
import  sys,os
import  shutil

# zip_file = zipfile.ZipFile('cmvn.zip','w')
# # 把zfile整个目录下所有内容，压缩为new.zip文件
# zip_file.write('cpptools/dist/cppcompile/',compress_type=zipfile.ZIP_DEFLATED)
# # 把c.txt文件压缩成一个压缩文件
# # zip_file.write('c.txt',compress_type=zipfile.ZIP_DEFLATED)
# zip_file.close()

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

global_path = "D:\myprogram\mytools"



if __name__ == "__main__":
    roottop = os.getcwd()
    os.chdir('cpptools')
    os.system('pyinstaller -D cppcompile.py')
    if os.path.exists('dist/cppcompile'):
        os.chdir("dist/cppcompile")
        print(os.getcwd())
        zip_file = zipfile.ZipFile('cmvn.zip','w')
        #
        rootpath = os.getcwd()
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == 'cppcompile.exe':
                    os.rename(name, "cmvn.exe")
                    zip_file.write("cmvn.exe",compress_type=zipfile.ZIP_DEFLATED)
                    continue
                if name != 'cmvn.zip':
                    f= os.path.join(root, name)
                    print(f.split(rootpath+"\\")[-1])
                    zip_file.write(f.split(rootpath+"\\")[-1],compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()
        shutil.copy2('cmvn.zip',roottop+'\\'+'cmvn.zip' )
        #
        os.chdir(roottop+"\\"+'cpptools')
        delfiles = ["dist","build","__pycache__"]
        for c in delfiles:
            del_file(c)
            try:
                os.rmdir(c)
            except:
                pass
        os.remove("cppcompile.spec")
        #
        os.chdir(roottop)
        shutil.copy2('cmvn.zip',global_path+'\\'+'cmvn.zip' )
    
    else:
        print("目录 cpptools/dist/cppcompile 不存在 ")
