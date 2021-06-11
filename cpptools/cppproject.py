#!/usr/bin/env python
# -*- coding:utf-8 -*-

from   pom import Pom
from   pub import *
import os,logging,platform
import template  as tp
from   typing import List
import re,time


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


class MavenAutoTools(object):
    def __init__(self,pom):
        self.rootpath  = os.getcwd()
        self.pom       = Pom(pom)

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

    def get_child_module_pom(self, moduel_info, version):
        '''
        解析子模块pom.xml文件
        '''
        moduel_info = moduel_info.split('.')
        src_module_addr = join_change_path(default_libpath, moduel_info, version)+'\pom.xml'
        return Pom(src_module_addr)

    def pull_transform_libs_path(self, moduel_info, version ):
        '''
        转化lib库路径  lrts.ws.interface
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        #解析子模块pom
        childpom = self.get_child_module_pom(moduel_info, version)
        moduel_info = moduel_info.split('.')
        src_addr = join_change_path(default_libpath, moduel_info, version)
        src_addr = join_change_path(src_addr, childpom.lib)+'.lib'
        if not childpom.lib: #无库文件
            return None
        dest_addr = join_change_path(os.getcwd(),['lib','Windows','%s.lib'%(childpom.lib[0])] )
        return [src_addr, dest_addr ]

    def pull_transform_header_path(self,moduel_info, version):
        '''
        转化头文件路径
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        childpom = self.get_child_module_pom(moduel_info, version)
        moduel_info = moduel_info.split('.')
        src_addr_prefix = join_change_path(default_libpath, moduel_info, version)

        if not childpom.header: #无头文件
            return None
        #遍历拉取所有头文件
        for h in childpom.header:
            src_addr  = os.path.join(src_addr_prefix, h) 
            if not childpom.header_prefix:
                dest_addr = join_change_path(os.getcwd(),['include','%s'%(h)] )
            else:
                temp = ['include'] + childpom.header_prefix + ['%s'%(h)]
                dest_addr = join_change_path(os.getcwd(),temp )
            copy_file(src_addr, dest_addr )


    def pull_transform_pom_path(self,moduel_info, version):
        '''
        转化pom路径
        :return: 源地址文件绝对路径, 目的地绝对路径
        '''
        temp = moduel_info
        moduel_info = moduel_info.split('.')
        src_addr = join_change_path(default_libpath, moduel_info, version)
        src_addr = join_change_path(src_addr, ['pom.xml'])
        dest_addr = join_change_path(os.getcwd(), ['pom','pom-%s-%s.xml'%(temp,version)])
        return [src_addr, dest_addr]

    def push_libs_to_repository(self, moduel_info, version=None ):
        '''
        将本地.lib文件安装到本地仓库
        :return:
        '''
        moduel_info = moduel_info.split('.')
        repository_addr = join_change_path(default_libpath, moduel_info, self.pom.version[0])
        repository_addr = os.path.join(repository_addr,"%s.lib"%(self.pom.lib[0]))
        src_addr = join_change_path(os.getcwd(), ["lib","Debug","%s.lib"%(self.pom.lib[0])])
        return [repository_addr, src_addr]

    def push_pom_to_repository(self, moduel_info, version=None ):
        '''
        将本地pom文件安装到本地仓库
        :return:
        '''
        moduel_info = moduel_info.split('.')
        repository_addr = join_change_path(default_libpath, moduel_info, self.pom.version[0])
        repository_addr = os.path.join(repository_addr,'pom.xml')
        src_addr = join_change_path(os.getcwd(), ['pom.xml'])
        return [repository_addr, src_addr]

    def push_header_to_repository(self, moduel_info, version=None ):
        '''
        将本地头文件文件安装到本地仓库
        :return:
        '''
        moduel_info = moduel_info.split('.')
        repository_addr = join_change_path(default_libpath, moduel_info, self.pom.version[0])
        if not self.pom.header:
            logging.info(" "+ moduel_info + "no .h want to other moduel ")
            return 
        for h in self.pom.header:
            dest_addr = os.path.join( repository_addr, h )
            if not self.pom.header_prefix:
                src_addr  = join_change_path( os.getcwd(), ["src",'include', h ])
            else:
                temp = ["src",'include'] + self.pom.header_prefix + [h]
                src_addr  = join_change_path( os.getcwd(), temp )
            copy_file(src_addr, dest_addr )

    def install_all_interface_files(self):
        '''
        安装本模块的输出文件 .pom .lib .h
        '''
        try:
            #安装pom文件
            moduel_info = self.pom.groupid[0]+'.'+self.pom.groupid[1]+'.'+self.pom.artifactId[0]
            ret = self.push_pom_to_repository(moduel_info, self.pom.version)
            #print(ret)
            copy_file(ret[1], ret[0])
            #安装头文件
            self.push_header_to_repository(moduel_info, self.pom.version)

            #安装库文件
            ret = self.push_libs_to_repository(moduel_info, self.pom.version)
            #print(ret)
            copy_file(ret[1], ret[0])
            print('\n %s install files success  '%(moduel_info) )
            print(" moduel  version: %s"%(self.pom.version[0] ))
        except:
            print('\n %s install files fail  '%(moduel_info) )
            print(" moduel  version: %s"%(self.pom.version[0] ))



    def repo_dependencys_file(self):
        '''
        获取远程/本地仓库中 .lib .h .pom文件
        '''
        print("======================dependencies=============================")
        #遍历依赖的模块
        for key,value in self.pom.get_dependencies().items():
            temp = key.split('.')
            lastversion = self.get_last_version(temp[:-1:], [temp[-1]])
            if value: #获得指定版本
                #安装pom文件
                ret = self.pull_transform_pom_path(key, value )
                copy_file(ret[0], ret[1])
                # 安装头文件
                self.pull_transform_header_path(key,value )

                # 安装库文件
                ret = self.pull_transform_libs_path(key,value )
                if ret: copy_file(ret[0], ret[1])
                print(key.ljust(30,' ')+'version: %s'%(value))
            else:  #获得最新版本
                ret = self.pull_transform_pom_path(key, lastversion)
                copy_file(ret[0], ret[1])
                # 安装头文件
                self.pull_transform_header_path(key,lastversion)

                if ret: ret = self.pull_transform_libs_path(key,lastversion )
                copy_file(ret[0], ret[1])
                print(key.ljust(30,' ')+'version: %s'%(lastversion))
        print("======================dependencies=============================\n")



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
            pom.repo_dependencys_file()
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
            pom.install_all_interface_files()
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