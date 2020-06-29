# -*- encoding: utf-8 -*-
#@File    : repo.py
#@Time    : 2020/6/18 21:52
#@Author  : Lancer

import sys
import shutil
import os,re,logging
import hashlib, codecs
from   config import  *
from   util import *
from   pom  import  Pom

'''
格式：
protocol.h =>  windows0.0.1@protocol.h  -> windows0.0.1@protocol.h.md5
'''

class  ManageLib(object):
    def __init__(self, pomfile ):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        try:
            readpom = Pom(pomfile)
            self.depandency = readpom.get_dependency()
            self.groupid_artifactid =  readpom.get_maven_path()+"."+readpom.get_moduel_name()
            self.version = readpom.get_out_version()
            self.libname =  readpom.get_outlib()
            self.headname = readpom.get_outheader()
            self.rootpath = os.getcwd()
        except  FileNotFoundError:
            logging.info("No pom: %s "%(os.getcwd()+"\\"+pomfile))
        #self.dst_path = default_libpath + "\\" + self.groupid_artifactid.replace(".", "\\") + "\\"+self.version

        # logging.info(self.depandency)
        # logging.info(self.groupid_artifactid+"."+ self.version)
        # logging.info(self.libname)
        # logging.info(self.headname)


    def get_max_version(self, groupid_artifactId):
        dst_path = default_libpath + "\\" + groupid_artifactId.replace(".", "\\") + "\\"+self.version
        try:
            version_dir  = os.path.dirname(dst_path)
            versions = os.listdir(version_dir)
            if not versions:
                logging.info("%s  not exist version dir"%(groupid_artifactId))
            else:
                return  max(versions)
        except Exception as e:
            logging.info("%s  not exist dir"%(groupid_artifactId))
        return  None

    def  install_files(self):
        '''
        安装库文件等到本地目录
        '''
        dst_path = default_libpath + "\\" + self.groupid_artifactid.replace(".", "\\") + "\\"+self.version
        src_lib =   os.getcwd()+"\\"+"lib\\Debug\\%s.lib"%(self.libname)
        src_hhp =   os.getcwd()+"\\"+"src\\include\\%s"%(self.headname[0])
        dst_lib =   dst_path+"\\%s.lib"%self.get_full_name(self.version, "%s"%(self.libname))[0]
        dst_hhp =   dst_path+"\\%s"%self.get_full_name(self.version, "%s"%(self.headname[0]))[0]
        copy_file(srcfile=src_lib, dstfile= dst_lib  )
        copy_file(srcfile=src_hhp, dstfile= dst_hhp  )
        print("success ",dst_lib.split('\\')[-1] )
        print("success ",dst_hhp.split('\\')[-1] )


    def  repo_files(self):
        child_path = []
        for i in range(len(self.depandency)):
            #print(self.depandency[i]["artifactId"])
            dst_path = ""
            if "version" in self.depandency[i].keys():
                #print(self.depandency[i]["version"])
                dst_path = default_libpath + "\\" + self.depandency[i]["artifactId"].replace(".", "\\") + "\\"+self.depandency[i]["version"]
            else:
                if None == self.get_max_version(self.depandency[i]["artifactId"]):
                    logging.info("find fail : %s "%(self.depandency[i]["artifactId"]))
                    continue
                else:
                    pass
                    #print("max version：", self.get_max_version(self.depandency[i]["artifactId"]))
                dst_path = default_libpath + "\\" + self.depandency[i]["artifactId"].replace(".", "\\") + "\\"+self.get_max_version(self.depandency[i]["artifactId"])
            child_path.append(dst_path)
        #print(child_path)
        
        for i in range(len(child_path)):
            try:
                os.chdir(child_path[i])
                files = os.listdir()
                #print(files)
                for file in files:
                    if file.endswith(".lib"):
                        for iter_file in  self.get_short_name(file):
                            copy_file(srcfile= child_path[i]+"\\"+file, dstfile= self.rootpath+"\\"+"lib\\Windows\\%s"%(iter_file)  )
                            print("==src==",child_path[i]+"\\"+file)
                            print("==dst==",self.rootpath+"\\"+"lib\\Debug\\%s"%(iter_file))
                    elif file.endswith(".h"):
                        for iter_file in  self.get_short_name(file):
                            copy_file(srcfile= child_path[i]+"\\"+file, dstfile= self.rootpath+"\\"+"include\\%s"%(iter_file)  )
                            print("==src==",child_path[i]+"\\"+file)
                            print("==dst==",self.rootpath+"\\"+"include\\%s"%(iter_file))
            except FileNotFoundError:
                logging.info("repo fail : %s "%(child_path[i]))



    def get_short_name(self, *files_name ):
        '''
        将转化后的文件名还原为原始文件
        '''
        ret = []
        for i in range(len(files_name)):
            if False == files_name[i].split("@")[-1].endswith(".md5"):
                ret.append( files_name[i].split("@")[-1] )
        return ret

    def get_full_name(self,vesrion, *files_name):
        '''
        原始文件名获得转化后的文件名
        '''
        ret = []
        for i  in range(len(files_name)):
            ret.append("windows%s@%s"%(vesrion,files_name[i] ))
        return ret
    

    def get_md5str(self,filename):
        '''
        获得文件的md5 值
        '''
        with open(filename) as f:
            return f.read()

    def cal_md5(self,filename):
        '''
        计算文件的md5值
        '''
        m = hashlib.md5()
        with open(filename, 'rb') as f:
            m.update(f.read())
            return m.hexdigest()



if __name__ == '__main__':
    test = ManageLib("pom.xml")
    #print(test.get_max_version("com.lancer.protocol"))
    test.repo_files()
    #test.install_files()

