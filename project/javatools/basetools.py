#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-06-16 11:14:37

import os,sys,re,shutil,binascii


def run_cmd( cmds, src_path="", back_path="" ):
    if src_path:
        try:
            os.chdir(src_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s"%(src_path))
        finally:
            os.chdir(os.getcwd())
    if isinstance(cmds,str):
        os.system(cmds)
    elif isinstance(cmds,list) or isinstance(cmds,tuple):
        for cmd in cmds:
            os.system(cmd)
    elif isinstance(cmds,dict):
        for key,value in cmds.items():
            try:
                key(value)
            except Exception as e :
                #print("=== function: %s cmd: %s "%(str(key),str(value) ))  
                print("=== err: ", e)      
    else:
        print("=== unexpect  input data type")
    if back_path:
        try:
            os.chdir(back_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s  "%(back_path))
        finally:
            os.chdir(os.getcwd())

def  get_cwd_file(file_type, isdir = False):
    ret = []
    files = os.listdir(os.getcwd())
    for file in files:
        if isdir == False:
            if file_type == file.split(".")[-1]:
                ret.append(file)
        else:
            if os.path.isdir(file):
                ret.append(file)
    return ret 


# def get_file(file_type):
#     ret = []
#     for root, dirs, files in os.walk(os.getcwd(),topdown=True):
#         for name in files:
#             if name.split(".")[-1] == file_type:
#                 ret.append(os.path.join(root, name))
#         # for name in dirs:
#         #     print(os.path.join(root, name)) 
#     return ret 
