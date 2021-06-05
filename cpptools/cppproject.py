#!/usr/bin/env python
# -*- coding:utf-8 -*-

from   pom import Pom
from   pub import *
import os,logging,platform
import template  as tp
from typing import List


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


class MavenAutoTools(object):
    def __init__(self,pom):
        self.rootpath  = os.getcwd()
        self.pom       = Pom(pom)
        # 安装本地文件

        # 获得依赖文件

    def get_last_version(self, groupid, artifactId ):
        '''
        获得最新版本号  None未install过文件
        '''
        groupid.extend(artifactId)
        basedir = join_change_path( default_libpath, groupid )
        is_dirs_exists(basedir,True)
        os.chdir(basedir)
        versions = []
        for root, dirs, files in os.walk(basedir):
            for dir in dirs:
                versions.append(dir)
            break
        os.chdir(self.rootpath)  #chage dirs
        if versions:
            return max(versions)
        else:
            return None

    def pull_transform_libs_path(self, moduel_info, version=None ):
        '''
        转化lib库路径  lrts.ws.interface
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        moduel_info = moduel_info.split('.')
        if not version: version = self.get_last_version(moduel_info[:-1:], [moduel_info[-1]] )
        src_addr = join_change_path(default_libpath, moduel_info, version)
        src_addr = join_change_path(src_addr, self.pom.lib)+'.lib'
        dest_addr = join_change_path(os.getcwd(),['lib','Windows','%s.lib'%(self.pom.lib[0])] )
        return [src_addr, dest_addr ]

    def pull_transform_header_path(self,moduel_info, version=None):
        '''
        转化头文件路径
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        moduel_info = moduel_info.split('.')
        if not version: version = self.get_last_version(moduel_info[:-1:], [moduel_info[-1]] )
        src_addr = join_change_path(default_libpath, moduel_info, version)
        src_addr = join_change_path(src_addr, self.pom.header)
        dest_addr = join_change_path(os.getcwd(),['include','%s'%(self.pom.header[0])] )
        return [src_addr, dest_addr ]

    def pull_transform_pom_path(self,moduel_info, version=None):
        '''
        转化pom路径
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        moduel_info = moduel_info.split('.')
        if not version: version = self.get_last_version(moduel_info[:-1:], [moduel_info[-1]])
        src_addr = join_change_path(default_libpath, moduel_info, version)
        src_addr = join_change_path(src_addr, ['pom.xml'])
        dest_addr = join_change_path(os.getcwd(), ['pom','pom.xml'])
        return [src_addr, dest_addr]


    def push_transform_header_path(self,moduel_info, version=None):
        pass


    def push_libs_to_repository(self):
        '''
        将本地.lib .h .pom文件安装到本地仓库
        :return:
        '''
        return True

    def repo_dependencys_file(self):
        '''
        获取远程/本地仓库中 .lib .h .pom文件
        :return:
        '''
        return False





class  ManageLibs(object):
    def __init__(self,pompath):
        self.rootpath    = os.getcwd()
        self.pom         = None
        self.dependencys = None

    def get_pom_info(self,pom):
        '''
        获得pom信息
        '''
        return Pom(pom)

    def get_dependencys(self,pom):
        self.dependencys = Pom(pom).dependencies



    def install_local_file(self,groupid_artifactid):
        '''
        安装头文件  库到本地仓库
        '''
        pass

    def repo_dependencys_file(self):
        '''
        拉取本模块依赖的头文件及库
        '''

    def repo_dependency_sigle(self):
        pass





def create_project(project_info:str):
    project_str = project_info
    if project_str.count(r'.') != 2:
        logging.info("project format err like ==> com.lancer.moduelname")
        return
    groupId = ".".join(project_str.split('.')[0:-1:])
    moduelname = project_str.split('.')[-1]
    logging.info("groupId: %s  moduel_name: %s " % (groupId, moduelname))
    # create  file
    create_file(r'CMakeLists.txt', tp.topcmake % ({"prjname": moduelname}))
    create_file(r"src/CMakeLists.txt", tp.src_leve_cmake % ({"prjname": moduelname}))
    # write  cppunit  test file
    create_file(r"src/test_cppunit/%s_test.cpp" % (moduelname), (tp.cppunit_testfile % ({"prjname": moduelname})))
    create_file(r"src/test_cppunit/main_cppunit.cpp", tp.cppunit_testmain)
    # write  cpp/h  src file
    create_file(r"src/main/%s.cpp" % moduelname, tp.cppfile_template)
    create_file(r"src/include/%s.h" % moduelname, tp.hhp_template % ({"prjname": moduelname.upper()}))
    # ftest
    create_file(r"src/ftest/ftest.cpp", tp.cppfile_template_lintcode)
    create_file(r"readme.md", tp.readme_template)
    create_file(r"pom.xml", tp.pom_template % ({"groupId": groupId, "prjname": moduelname}))


class  CppProject(object):
    def __init__(self,pom):
        self.rootpath = os.getcwd()
        #self.pom = Pom(pom)

    def cppproject_init(self):
        new_dir = [r'projects/bdef', r'bin/Debug', r'include', r'pom']
        if "Windows" == platform.system():
            new_dir.append(r'lib/Windows')
        elif "Linux" == platform.system():
            new_dir.append(r'lib/Linux')
        for dir in new_dir:
            make_dirs(dir)
        ###############
        if os.path.exists("pom.xml"):
            os.chdir(self.rootpath)
            ### 拉取依赖库 及头文件
            print("=======================================")
            #pull_local_file(self.pom.dependencies)
            print("=======================================")
            ###
            os.chdir(r'projects/bdef')
            os.system("cmake  ../.. && cd ../..")
        else:
            logging.info("dir not exist pom.xml")

    def cppproject_build(self):
        os.system(r'cmake --build projects/bdef')


    def cppproject_install(self):
        if os.path.exists("pom.xml"):
            #push_local_file()
            print("install files ")
        else:
            logging.info("pom.xml not exist  install fail ")

    def cppproject_utest(self):
        if True == os.path.exists(r'bin/Debug'):
            os.chdir(r'bin/Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('cppunit') and platform.system() == "Windows":
                    os.system(name)
                    break
                elif name.startswith('t') and platform.system() == "Linux":
                    print("====================Linux====================\n")
                    os.system('./%s' % (name))
                    break
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_ftest(self):
        if True == os.path.exists(r'bin/Debug'):
            os.chdir(r'bin\Debug')
            exenames = os.listdir(os.getcwd())
            for name in exenames:
                if name.endswith('.exe') and name.startswith('ftest') and platform.system() == "Windows":
                    os.system(name)
                    break
                elif name.startswith('ftest') and platform.system() == "Linux":
                    print("====================Linux====================\n")
                    os.system('./%s' % (name))
                    break
        else:
            logging.info("not find dir bin\Debug ")

    def cppproject_updateversion(self, dst_version):
        logging.info("升级版本号to: %s"%dst_version)

    def  cppproject_clean(self):
        logging.info("clean project file")
        delfile(filepath=os.path.join(os.getcwd(),'bin'))
        delfile(filepath=os.path.join(os.getcwd(),'projects'))
        delfile(filepath=os.path.join(os.getcwd(),'pom'))
        delfile(filepath=os.path.join(os.getcwd(),'lib'))
        delfile(filepath=os.path.join(os.getcwd(),'include'))



if __name__ == '__main__':
    test = CppProject('pom.xml')