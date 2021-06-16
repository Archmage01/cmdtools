#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,re 
from   pom import Pom
from   pub import *

class MavenAutoTools(object):
    def __init__(self, pom):
        self.rootpath  = os.getcwd()
        self.pom       = Pom(pom)

    def get_last_version(self,  unique_project ):
        '''
        获得最新版本号  None未install过文件
        '''
        unique_project = unique_project.split('.')
        basedir = default_libpath
        for c in unique_project:
            basedir = os.path.join(basedir, c )
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

    def  get_child_module_pom(self, unique_project, version, flag ="pull"):
        '''
        解析子模块pom.xml文件
        '''
        if 'push' == flag: return Pom('pom.xml')
        unique_project = unique_project.split('.')
        pom_file = default_libpath
        for c in unique_project:
            pom_file = os.path.join(pom_file, c )
        pom_file = os.path.join(pom_file, version, 'pom.xml' )
        #print(pom_file)
        return Pom(pom_file)

    def transform_lib_absolute_address(self, unique_project, version, platform="Windows", flag ="pull"):
        '''
        :param  unique_project:    类似 com.utest.cppunit
        :param  version :          版本号 0.0.1
        :param  platform:          Windows Linux
        :param  flag    :          pull    push
        return: {'project': None , 'depository':None }
        '''       
        childpom       = self.get_child_module_pom( unique_project, version, flag)
        ret =  {'project': None , 'depository':None }
        if not childpom.lib: #无库文件
            return None
        unique_project = unique_project.split('.')
        if "Windows" == platform:
            if "pull" == flag:
                project    = os.path.join(os.getcwd(), 'lib','Windows','%s.lib'%(childpom.lib[0]) )
            else:
                project    = os.path.join(os.getcwd(), 'lib','Debug','%s.lib'%(childpom.lib[0]) )

            depository = os.path.join(default_libpath,unique_project[0],unique_project[1],unique_project[2])
            depository = os.path.join(depository, version ,childpom.lib[0]+'.lib' )
        elif "Linux" == platform:
            if "pull" == flag:
                project    = os.path.join(os.getcwd(), 'lib','ARMCC','lib%s.a'%(childpom.lib[0]) )
            else:
                project    = os.path.join(os.getcwd(), 'lib',"ARMCC",'lib%s.a'%(childpom.lib[0]) )
            depository = os.path.join(default_libpath,unique_project[0],unique_project[1],unique_project[2])
            depository = os.path.join(depository, version , 'lib%s.a'%(childpom.lib[0])  )
        else:
            pass
        ret['project'], ret['depository'] = project, depository
        return ret 

    def transform_pom_absolute_address(self, unique_project, version, flag ="pull"):
        '''
        :param  unique_project:    类似 com.utest.cppunit
        :param  version :          版本号 0.0.1
        :param  flag    :          pull    push
        return: {'project': None , 'depository':None }
        '''        
        childpom       = self.get_child_module_pom( unique_project, version,flag )
        temp = unique_project
        ret =  {'project': None , 'depository':None }
        if not childpom.lib: #无库文件
            return None
        unique_project = unique_project.split('.')
        if "push" == flag:
            project    = os.path.join(os.getcwd(), 'pom.xml' )
            depository = os.path.join(default_libpath,unique_project[0],unique_project[1],unique_project[2])
            depository = os.path.join(depository, version, 'pom.xml' )
        else:
            project    = os.path.join(os.getcwd(),'pom', 'pom-%s-%s.xml'%(temp,version)  )
            depository = os.path.join(default_libpath,unique_project[0],unique_project[1],unique_project[2])
            depository = os.path.join(depository, version, 'pom.xml' )
        ret['project'], ret['depository'] = project, depository
        return ret 

    def transform_header_absolute_address(self, unique_project, version, flag ="pull"):
        childpom = self.get_child_module_pom(unique_project, version, flag)
        unique_project =  unique_project.split('.')
        if not childpom.header: return None #无需处理头文件
        if  'pull' == flag:
            depository_prefix = os.path.join(default_libpath, unique_project[0], unique_project[1],unique_project[2])
            depository_prefix = os.path.join(depository_prefix , version  )
            #遍历拉取所有头文件
            for header in childpom.header:
                depository = os.path.join(depository_prefix, header )
                if not childpom.header_prefix:
                    project = os.path.join(os.getcwd(), 'include', header )
                else:
                    project = os.path.join( os.getcwd(), 'include' )
                    for item in childpom.header_prefix:
                        project = os.path.join(project, item )
                    project = os.path.join(project, header )
                #copy
                copy_file( depository, project )
        else:
            depository_prefix = os.path.join(default_libpath, unique_project[0], unique_project[1],unique_project[2])
            depository_prefix = os.path.join(depository_prefix , version  )
            #遍历安装所有头文件
            for header in childpom.header:
                depository = os.path.join( depository_prefix, header )
                if not childpom.header_prefix:
                    project = os.path.join(os.getcwd(),'src','include', header )
                else:
                    project = os.path.join( os.getcwd(), 'src','include' )
                    for item in childpom.header_prefix:
                        project = os.path.join(project, item )
                    project = os.path.join(project, header )
                #copy
                copy_file( project, depository )
        return 0 

    def install_all_interface_files(self, platform="Windows"):
        try:
            moduel_info = self.pom.groupid[0]+'.'+self.pom.groupid[1]+'.'+self.pom.artifactId[0]
            # pom
            ret = self.transform_pom_absolute_address(moduel_info, self.pom.version[0], flag='push' )
            copy_file(ret['project'], ret['depository'])
            # header
            ret = self.transform_header_absolute_address(moduel_info, self.pom.version[0], flag='push' )

            if "Windows" == platform:
                # .lib
                ret = self.transform_lib_absolute_address(moduel_info, self.pom.version[0], platform="Windows",flag='push' )
                copy_file(ret['project'], ret['depository'])
            else:
                # .a
                ret = self.transform_lib_absolute_address(moduel_info, self.pom.version[0], platform="Linux",flag='push' )
                copy_file(ret['project'], ret['depository'])
            print('\n %s install files success  '%(moduel_info) )
            print(" moduel  version: %s"%(self.pom.version[0] ))
        except Exception as e:
            print('\n %s install files fail  '%(moduel_info) )
            print(" moduel  version: %s"%(self.pom.version[0] ))


    def repo_dependencys_file(self, platform="Windows"):
        print("\n======================dependencies=============================")
        for key,value in self.pom.get_dependencies().items():   
            lastversion = self.get_last_version(key)
            if value: #获得指定版本
                # pom 
                ret = self.transform_pom_absolute_address( key, value, flag='pull' )
                copy_file(ret['depository'], ret['project'])
                # header
                ret = self.transform_header_absolute_address( key, value, flag='pull' )
                if "Windows" == platform:
                    ret = self.transform_lib_absolute_address( key, value, platform="Windows",flag='pull' )
                    copy_file(ret['depository'], ret['project'])
                else:
                    ret = self.transform_lib_absolute_address( key, value, platform="Linux",flag='pull' )
                    copy_file(ret['depository'], ret['project'])
                print(key.ljust(30,' ')+'version: %s'%(value))
            else:
                # pom 
                ret = self.transform_pom_absolute_address( key, lastversion, flag='pull' )
                copy_file(ret['depository'], ret['project'])
                # header
                ret = self.transform_header_absolute_address( key, lastversion, flag='pull' )
                if "Windows" == platform:
                    ret = self.transform_lib_absolute_address( key, lastversion, platform="Windows",flag='pull' )
                    copy_file(ret['depository'], ret['project'])
                else:
                    ret = self.transform_lib_absolute_address( key, lastversion, platform="Linux",flag='pull' )
                    copy_file(ret['depository'], ret['project'])
                print(key.ljust(30,' ')+'version: %s'%(lastversion))
        print("======================dependencies=============================\n")
