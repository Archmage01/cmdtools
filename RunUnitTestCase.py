#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief:

import sys,os

def get_file(file_type):
    ret = []
    for root, dirs, files in os.walk(os.getcwd(),topdown=True):
        for name in files:
            if name.split(".")[-1] == file_type:
                ret.append(os.path.join(name))
        # for name in dirs:
        #     print(os.path.join(root, name)) 
    return ret

if __name__ == '__main__':
    os.chdir('test')
    ret = get_file('py')
    for file in ret:
        os.system("python %s"%(file))
    #print(ret)