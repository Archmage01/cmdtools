# -*- encoding: utf-8 -*-
#@File    : pom.py
#@Time    : 2020/6/19 22:43
#@Author  : Lancer

import os,sys,re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

'''
如果使用Element.findall()或者Element.find()方法，
  则只会从结点的直接子结点中查找，并不会递归查找。 iter() 递归
  text  attrib  tail
'''

class  Pom(object):
    def __init__(self, pomfile ):
        self.tree = ET.parse(pomfile)
        self.root = self.tree.getroot()
        self.groupId_artifactId = self.get_maven_path() +"."+self.get_moduel_name()
        self.out_lib  = self.get_outlib()
        self.out_header = self.get_outheader()
        self.version =  self.get_out_version()
        self.dependencies = self.get_dependency()

        # print("id: ",self.groupId_artifactId )
        # print("输出库: ",self.out_lib)
        # print("输出头文件: ",self.out_header)
        # print("版本号:",self.version)
        # for i in range(len(self.dependencies)):
        #     print(self.dependencies[i])

    def  get_dependency(self):
        ret = []
        for dependency in self.root.iter("dependency"):
            child = [None,None]
            for artifactId in dependency.iter("artifactId"):
                child[0] = artifactId.text
            for version in dependency.iter("version"):
                child[1] = version.text
            ret.append(child)
        return ret

    def get_maven_path(self):
        for groupId in self.root.iter("groupId"):
            return  groupId.text

    def get_outlib(self):
        for project in self.root.iter("project"):
            for lib in project.iter("lib"):
                return lib.text
    
    def get_out_version(self):
        for project in self.root.iter("project"):
            for lib in project.findall("version"):
                return lib.text

    def  get_moduel_name(self):
        for project in self.root.iter("project"):
            for groudname in project.iter("artifactId"):
                return groudname.text

    def get_outheader(self):
        ret = []
        hh_path = ""
        for header_prefix in self.root.iter("header_prefix"):
            hh_path = header_prefix.text
        for header in  self.root.iter("header"):
            if  hh_path:
                ret.append(hh_path+"."+ header.text)
            else:
                ret.append(header.text)
        return ret



if __name__ == '__main__':
    test = Pom("pom.xml")
    