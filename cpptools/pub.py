#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import re
import getpass
import logging
import shutil
import platform

logging.basicConfig(level=logging.INFO, format='===cmvn===  %(message)s')


### 默认项目路径  库 头文件  源文件等目录
default_libpath       = os.path.join(os.path.expanduser('~'),'.mavenlib')
default_src_prefix    = "src"
default_header_prefix = "include"
default_bin_prefix    = 'bin'
default_lib_prefix    = 'lib'
default_sys_prefix    = ''
default_project_top_prefix = 'project'
default_project_prefix     = 'bdef'
default_buildinfo_name     = 'tools-build-info'

src_header_prefix ="include"
src_main_prefix   = "main"
src_test_prefix   = "test"
src_ftest_prefix  = "ftest"

### 默认后缀一般文件类型
default_lib_suffix    = ""
default_header_suffix = ".h"
default_target_suffix = ".exe"

### 平台相关
if  platform.system() == "Windows":
    default_sys_prefix = 'Windows'
    default_lib_suffix = '.lib'
elif platform.system() == "Linux":
    default_libpath       = os.path.expanduser('~')+"/mavenlib"
    default_sys_prefix = 'Linux'
    default_lib_suffix = '.a'
else:
    default_sys_prefix = "unknowsys"

def create_file(filename, content, encoding_str="utf-8"):
    '''
    创建文件 默认UTF-8
    filename: 文件名(含路径)
    content:  文件内容
    '''
    old_path = os.getcwd()
    name = filename.split("/")[-1]
    filepath = "/".join(filename.split("/")[0:-1:])
    if filepath:
        if False == os.path.exists(filepath):
            os.makedirs(filepath)
        os.chdir(filepath)
    with open(name, mode="w", encoding=encoding_str) as file:
        file.write(content)
        file.close()
    os.chdir(old_path)
    logging.info("create file success: [ %s ] " % (filename))



def open_file(filename):
    try:
        with open(filename, mode="r", encoding='utf-8') as file:
            return [file.read(), 'utf-8']
    except UnicodeDecodeError:
        with open(filename, mode="r", encoding='gbk') as file:
            return [file.read(),'gbk']
    except IOError:
        logging.info("cannot find file: %s " % (filename))
        return None


def make_dirs(new_dir, topath=False):
    # 'project/debug/test'
    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
            logging.info(" make dir %s " % (new_dir))
        except Exception as e:
            print(e)
        finally:
            if topath == True:
                os.chdir(new_dir)


def run_cmd(cmds, src_path="", back_path=""):
    pass


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

def delall(abpath):
    try:
        if os.path.exists(abpath):
            if os.path.isdir(abpath):
                shutil.rmtree(abpath)
            else:
                os.remove(abpath)
    except Exception as e:
        print("del dir=%s  err"%(abpath))
        

def join_change_path(prefix_path:str, mb_list, max_version=None ):
    '''
    转化路径 拼接路径
    :param prefix_path:  默认libpath
    :param mb_list    :  artifactId, groupid
    :param max_version:  None 默认版本  other 实际版本号
    :return:
    '''
    ret = os.path.join(prefix_path,*mb_list)
    if max_version:
        ret = os.path.join(ret,max_version)
    return  ret

def is_dirs_exists(dirs, createdir=None):
    '''
    判断目录是否存在
    :param dirs     :  目录
    :param createdir:  None不新建 True:若目录不存在则新建目录
    :return: True 目录存在   False 目录不存在
    '''
    if os.path.isdir(dirs):
        return True
    else:
        if createdir:
            os.makedirs(dirs)
            return True
    return False


def is_file_exists(filespath, createdir=None):
    '''
    判断目录下文件是否存在
    :param filespath:  文件绝对路径
    :param createdir:  None不新建 True:若目录不存在则新建目录
    :return : True 文件存在   False 文件不存在
    '''
    if os.path.isfile(filespath):
        return True
    else:
        if platform.system() == "Windows":
            if createdir:
                path = '\\'.join(filespath.split('\\')[0:-1:])
                is_dirs_exists(path,True)
        else:
            if createdir:
                path = '/'.join(filespath.split('\\')[0:-1:])
                is_dirs_exists(path,True)
    return False

def copy_file(srcfile, dstfile):
    '''
    复制文件
    :param srcfile: 源文件地址
    :param dstfile: 目的地址
    '''
    if True != is_file_exists(srcfile):
        logging.error("err:  src file not exists %s"%(srcfile))
        return False
    else:
        is_file_exists(dstfile,createdir=True) #目录不存在就创建
        try:
            shutil.copy2(srcfile, dstfile)
            return True
        except:
            logging.error("copy fail: %s to  %s" % (srcfile, dstfile))
            return False
            
def path_join(path,  *paths):
    ret = os.path.join(path,*paths)
    if platform.system() != "Windows":
        ret = ret.replace('\\', '/')
    return ret


global_cmd = {}


if __name__ == "__main__":
    os.path.join(path)
    pass