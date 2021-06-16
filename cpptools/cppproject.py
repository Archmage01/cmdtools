#!/usr/bin/env python
# -*- coding:utf-8 -*-

from   pom import Pom
from   pub import *
import os,logging,platform
import template  as tp
from   typing import List
import re,time
from   mavenautotools import MavenAutoTools



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
    create_file(r"src/main/%s.c" % moduelname, tp.cppfile_template)
    create_file(r"src/main/ver_%s.c" % moduelname, tp.ver_module_template%({"prjname": moduelname}))
    create_file(r"src/include/%s.h" % moduelname, tp.hhp_template % ({"prjname": moduelname.upper()}))
    # ftest
    create_file(r"src/ftest/ftest.cpp", tp.cppfile_template_lintcode)
    create_file(r"readme.md", tp.readme_template)
    create_file(r"pom.xml", tp.pom_template % ({"groupId": groupId, "prjname": moduelname}))
    # arm cmake 
    create_file(r"cmake/arm.cmake", tp.armcmake_template)
    create_file(r"cmake/common.cmake", tp.common_template)



class  CppProject(object):
    def __init__(self,pom):
        self.rootpath = os.getcwd()

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
            pom = MavenAutoTools('pom.xml')
            pom.repo_dependencys_file(platform="Windows")
            ###
            os.chdir(r'projects/bdef')
            os.system("cmake  ../.. && cd ../..")
        else:
            logging.info("dir not exist pom.xml")

    def cppproject_build(self):
        os.system(r'cmake --build projects/bdef')


    def cppproject_install(self):
        if os.path.exists("pom.xml"):
            #安装文件到本地仓库
            pom = MavenAutoTools('pom.xml')
            pom.install_all_interface_files(platform="Windows")
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

    def check_version(self, dst_version ):
        #检查版本号
        pattern = re.compile(r'\d{1}\.\d{1,2}\.\d{1,2}?')
        result = pattern.match(dst_version)
        if not result:
            print('\n=== version err: %s please check version'%(dst_version))
            return False
        else:
            return True

    def cppproject_updateversion(self, dst_version):
        #logging.info("升级版本号to: %s"%dst_version)
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if not self.check_version(dst_version): return 
        #修改pom文件 
        pom = Pom('pom.xml')
        old_version = pom.version[0]
        ret = open_file('pom.xml')
        if ret:
            content, charset = ret[0],ret[1]
            with open('pom.xml', mode="w+", encoding=charset) as file:
                content = re.sub(r'\<version\>.*\<\/version\>',"<version>%s</version>"%(dst_version), content, 1 )
                file.write(content)
                file.close()
        else:
            logging.info(" auto update version pom.xml fail ")
        #修改.c文件中版本号
        pomfile= os.path.join(os.getcwd(),'src','main','ver_%s.c'%(pom.artifactId[0]))
        ret = open_file(pomfile)
        if ret:
            content, charset = ret[0],ret[1]
            with open(pomfile, mode="w+", encoding=charset) as file:
                temp = dst_version.split('.') 
                major,minor,patch = temp[0],temp[1],temp[2]  
                content = re.sub(r'\/\*- major\*\/\s{0,5}\d{1,3},',r'/*- major*/    %s,'%(major), content, 1 )
                content = re.sub(r'\/\*- minor\*\/\s{0,5}\d{1,3},',r'/*- minor*/    %s,'%(minor), content, 1 )
                content = re.sub(r'\/\*- patch\*\/\s{0,5}\d{1,3},',r'/*- patch*/    %s,'%(patch), content, 1 )
                content += "\n/* author: %s update version: %s time:%s  */"%(getpass.getuser(), dst_version, timestr )
                file.write(content)
                file.close()
        else:
            logging.info(" auto update version .c fail ")
        #修改单元测试中版本号
        utestfile= os.path.join(os.getcwd(),'src','test_cppunit','%s_test.cpp'%(pom.artifactId[0]))
        ret = open_file(utestfile)
        if ret:
            content, charset = ret[0],ret[1]
            with open(utestfile, mode="w+", encoding=charset) as file:
                temp = dst_version.split('.') 
                major,minor,patch = temp[0],temp[1],temp[2]  
                content = re.sub(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.major'%(pom.artifactId[0]),r'CPPUNIT_EASSERT( %s, ver_%s.major'%(major, pom.artifactId[0]), content, 1 )
                content = re.sub(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.minor'%(pom.artifactId[0]),r'CPPUNIT_EASSERT( %s, ver_%s.minor'%(minor, pom.artifactId[0]), content, 1 )
                content = re.sub(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.patch'%(pom.artifactId[0]),r'CPPUNIT_EASSERT( %s, ver_%s.patch'%(patch, pom.artifactId[0]), content, 1 )
                file.write(content)
                file.close()
        else:
            logging.info(" auto update version .cpp fail ")

        print("\n auto update version from: %s to %s  success "%( old_version,  dst_version ))

        

    def  cppproject_clean(self):
        print("clean project file")
        delfile(filepath=os.path.join(os.getcwd(),'bin'))
        delfile(filepath=os.path.join(os.getcwd(),'projects'))
        delfile(filepath=os.path.join(os.getcwd(),'pom'))
        delfile(filepath=os.path.join(os.getcwd(),'lib'))
        delfile(filepath=os.path.join(os.getcwd(),'include'))

    
    def auto_generate_file(self,filename):
        logging.info(filename)
        if filename.endswith('.h'):
            filename = filename.split('.')[0]
            create_file(r"src/include/%s.h" % filename, tp.hhp_template % ({"prjname": filename.upper()}))
        elif filename.endswith('.cpp'):
            filename = filename.split('.')[0]
            create_file(r"src/test_cppunit/%s_test.cpp" % (filename), (tp.cppunit_testfile % ({"prjname": filename})))
        else:
            pass
    
    def verify_version_nums(self):
        print("")
        #pom.xml 版本号
        pom = Pom('pom.xml')
        print( "pom.xml".ljust(30,' ')+'version: %s'%(pom.version[0]))
        #.c 版本号
        pomfile= os.path.join(os.getcwd(),'src','main','ver_%s.c'%(pom.artifactId[0]))
        ret = open_file(pomfile)
        if ret:
            content, charset = ret[0],ret[1]
            majorpattern = re.compile(r'\/\*- major\*\/\s{0,5}\d{1,3},')
            major = re.search(r'\d{1,3}', majorpattern.search(content).group())
            if major: major = major.group()
            minorpattern = re.compile(r'\/\*- minor\*\/\s{0,5}\d{1,3},')
            minor = re.search(r'\d{1,3}', minorpattern.search(content).group())
            if minor: minor = minor.group()
            patchpattern = re.compile(r'\/\*- patch\*\/\s{0,5}\d{1,3},')
            patch = re.search(r'\d{1,3}', patchpattern.search(content).group())
            if patch: patch = patch.group()
        cversion = major+"."+minor+"."+patch
        temp = "ver_%s.c "%(pom.artifactId[0])
        print( temp.ljust(30,' ')+'version: %s'%(cversion))
        #.cpp 版本号
        utestfile= os.path.join(os.getcwd(),'src','test_cppunit','%s_test.cpp'%(pom.artifactId[0]))
        ret = open_file(utestfile)
        if ret:
            content, charset = ret[0],ret[1]
            majorpattern = re.compile(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.major'%(pom.artifactId[0]))
            major = re.search(r'\d{1,3}', majorpattern.search(content).group())
            if major: major = major.group()
            minorpattern = re.compile(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.minor'%(pom.artifactId[0]) )
            minor = re.search(r'\d{1,3}', minorpattern.search(content).group())
            if minor: minor = minor.group()
            patchpattern = re.compile(r'CPPUNIT_EASSERT\(\s?\d{1,3},\s?ver_%s.patch'%(pom.artifactId[0]) )
            patch = re.search(r'\d{1,3}', patchpattern.search(content).group())
            if patch: patch = patch.group()
            utestversion = major+"."+minor+"."+patch
        temp = "%s_test.cpp "%(pom.artifactId[0])
        print( temp.ljust(30,' ')+'version: %s'%(utestversion))
        if pom.version[0] == utestversion and utestversion == cversion:
            print("校验版本号一致".center(30,"="))
        else:
            print(" 版本号不一致请检查 ".center(30,"="))

if __name__ == '__main__':
    test = CppProject('pom.xml')