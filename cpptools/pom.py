#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: pom

from lxml import etree

class Pom(object):
    def __init__(self, pom): #pom="pom.xml"
        self.pom  = etree.parse(pom)     #解析pom
        self.root = self.pom.getroot()   #获取根节点
        self.groupid       = [] #groupid
        self.artifactId    = [] #模块名
        self.version       = [] #模块版本号
        self.header_prefix = [] #头文件前缀路径
        self.header        = [] #头文件
        self.lib           = [] #库名
        self.dependencies  = {} #依赖模块唯一标识(groupid+模块名)

        self.get_moduel_base_info()
        self.get_dependencies()
        # self.printinfo()


    def printinfo(self):
        print(self.groupid)
        print(self.artifactId)
        print(self.version)
        print(self.header_prefix)
        print(self.header)
        print(self.lib)
        if self.dependencies:
            maxlen = max([len(v) for v in self.dependencies.keys()])
        #print(maxlen)
        for key,value in self.dependencies.items():
            print(" ", key.ljust(maxlen+1,' '),'value: ', value)


    def get_moduel_base_info(self):
        for node in self.root.getchildren():
            # match node tag  获取文本
            if 'groupId' == node.tag:
                self.groupid = node.text.strip().split('.')
            elif 'artifactId' == node.tag:
                self.artifactId = [node.text]
            elif 'version' == node.tag:
                self.version = [node.text]
            elif 'header_prefix' == node.tag:
                self.header_prefix = node.text.strip().split('/')
            elif 'header' == node.tag:
                self.header = [node.text]
            elif 'lib' == node.tag:
                self.lib = [node.text]
            else:
                pass

    def get_dependencies(self):
        last = None
        for dependency_node in self.root.xpath('//dependency'): #选取所有子元素dependency
            for node in  dependency_node.getchildren():
                if node.tag == "artifactId":
                    self.dependencies[node.text] = None
                    last = node.text
                elif node.tag == "version":
                    if last:
                        self.dependencies[last] = node.text
                    last = None
        return  self.dependencies





if __name__ == '__main__':
    pom = Pom('pom.xml')