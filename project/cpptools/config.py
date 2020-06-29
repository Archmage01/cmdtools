# -*- encoding: utf-8 -*-
#@File    : config.py
#@Time    : 2020/6/18 21:36
#@Author  : Lancer

import  os, sys,re,getpass
import  logging

default_libpath =  r"C:\Users\%s"%(getpass.getuser())+"\\.mavenlib"

## 设置日志格式
#logging.basicConfig(level=logging.INFO, format='[ %(filename)s %(lineno)d %(levelname)s] %(message)s')




if __name__ == '__main__':
    print(default_libpath)