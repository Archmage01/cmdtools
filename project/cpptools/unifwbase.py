#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Lancer  2020-07-20 12:03

import os
import sys
import re
import getpass
import logging
import shutil
import binascii

default_libpath = r"C:\Users\%s" % (getpass.getuser())+"\\.mavenlib"
logging.basicConfig(level=logging.INFO, format='%(message)s')


def create_file(filename, content, encoding_str="utf-8"):
    '''
    创建文件 默认UTF-8
    filename: 文件名(含路径)
    content:  文件内容
    '''
    old_path = os.getcwd()
    name = filename.split("\\")[-1]
    filepath = "\\".join(filename.split("\\")[0:-1:])
    if filepath:
        if False == os.path.exists(filepath):
            os.makedirs(filepath)
        os.chdir(filepath)
    with open(name, mode="w", encoding=encoding_str) as file:
        file.write(content)
        file.close()
    os.chdir(old_path)
    print("create file success: [ %s ] " % (filename))


def open_file(filename):
    try:
        with open(filename, mode="r", encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filename, mode="r", encoding='gbk') as file:
            return file.read()
    except IOError:
        print("cannot find file: %s " % (filename))


def copy_file(srcfile, dstfile):
    dir = "\\".join(dstfile.split("\\")[0:-1:])
    if not os.path.exists(dir):
        os.makedirs("\\".join(dstfile.split("\\")[0:-1:]))
    try:
        if not os.path.exists(srcfile):
            print("srcfile not exist: %s" % (srcfile))
        shutil.copy2(srcfile, dstfile)
    except FileNotFoundError:
        print("copy fail: %s to  %s" % (srcfile, dstfile))


def make_dirs(new_dir, topath=False):
    # r'project\debug\test'
    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
            print("===new dir %s " % (new_dir))
        except Exception as e:
            print(e)
        finally:
            if topath == True:
                os.chdir(new_dir)


def run_cmd(cmds, src_path="", back_path=""):
    if src_path:
        try:
            os.chdir(src_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s" % (src_path))
        finally:
            os.chdir(os.getcwd())
    if isinstance(cmds, str):
        os.system(cmds)
    elif isinstance(cmds, list) or isinstance(cmds, tuple):
        for cmd in cmds:
            os.system(cmd)
    elif isinstance(cmds, dict):
        for key, value in cmds.items():
            try:
                key(value)
            except Exception as e:
                #print("=== function: %s cmd: %s "%(str(key),str(value) ))
                print("=== err: ", e)
    else:
        print("=== unexpect  input data type")
    if back_path:
        try:
            os.chdir(back_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s  " % (back_path))
        finally:
            os.chdir(os.getcwd())


def get_max_version(groupid_artifactId):
    '''
    获得模块最新版本(最大版本号默认)
    '''
    dst_path = default_libpath + "\\" + groupid_artifactId.replace(".", "\\")
    try:
        # version_dir  = os.path.dirname(dst_path)  dst_path父目录
        # print(version_dir)
        versions = os.listdir(dst_path)
        if not versions:
            logging.info("%s  not exist version dir" % (groupid_artifactId))
        else:
            return max(versions)
    except Exception as e:
        logging.info("%s  not exist dir" % (groupid_artifactId))
    return None


def is_same_file(filename, fulldstname):
    """
     @brief is_same_file 首先判断修改大小，再判断修改时间，若都一致，初步判断一致
    """
    ret = False
    if os.path.exists(fulldstname):
        curstat = os.stat(filename)
        oldstat = os.stat(fulldstname)
        if (curstat.st_size == oldstat.st_size
                and int(curstat.st_mtime*1000) == int(oldstat.st_mtime*1000)
            ):
            ret = True
    return ret


def delfile(filepath=None, file=None):
    print(filepath)
    try:
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        if  file:
            if True == os.path.isfile(file):
                os.remove(file)
    except  Exception as e:
        print(e) 



global_cmd = {}
