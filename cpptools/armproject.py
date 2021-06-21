#!/usr/bin/env python
# -*- coding:utf-8 -*-

from   pom import Pom
from   pub import *
import os,logging,platform
import template  as tp
from   typing import List
import re,time
from   mavenautotools import MavenAutoTools


class  ArmProject(object):
    def __init__(self):
        self.rootpath = os.getcwd()

    def arm_project_init(self):
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
            pom = MavenAutoTools('pom.xml')
            pom.repo_dependencys_file(platform="Linux")
            ######################
            os.chdir(r'projects/bdef')
            cmake = self.rootpath + '\\cmake\\arm.cmake'
            cmds = "cmake  ../..  -G\"%s\" -DCMAKE_TOOLCHAIN_FILE=%s"%("MinGW Makefiles",cmake)
            print(cmds)
            os.system(cmds)
            os.chdir(self.rootpath)
        else:
            logging.info("dir not exist pom.xml")


    def arm_project_build(self):
        logging.info("arm_project_build")
        os.system(r'cmake --build projects/bdef')

    def arm_project_install(self):
        if os.path.exists("pom.xml"):
            #安装文件到本地仓库
            pom = MavenAutoTools('pom.xml')
            pom.install_all_interface_files(platform="Linux")
        else:
            logging.info("pom.xml not exist  install fail ")

    def arm_project_elf2bin(self):
        pom = Pom('pom.xml')
        debug_dir = os.path.join(os.getcwd(),'bin','Debug')
        if os.path.exists(debug_dir):
            os.chdir(debug_dir)
            for filename in os.listdir(debug_dir):
                #find .elf
                if filename.endswith('.elf'):
                    prefix = filename.split('.elf')[0]
                    tobin = "%s.bin"%(pom.artifactId[0])
                    tohex = "%s.hex"%(pom.artifactId[0])
                    try:
                        os.system("fromelf --bin --output=%s %s"%(tobin, filename ))
                        os.system("fromelf --vhx --output=%s %s"%(tohex, filename ))
                        print("\n create .bin or hex success ")
                    except:
                        print("\n create .bin or hex fail ")
        else:
            logging.info(" %s not exist please check ..."%(debug_dir))
        os.chdir(self.rootpath) 
