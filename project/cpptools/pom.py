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

        # for dependency in self.root.iter("dependency"):
        #     for artifactId in dependency.iter("artifactId"):
        #         print(artifactId.text)
        #     for version in dependency.iter("version"):
        #         print(version.text)

    def  get_dependency(self):
        ret = []
        for dependency in self.root.iter("dependency"):
            child = {}
            for artifactId in dependency.iter("artifactId"):
                child["artifactId"] = artifactId.text
            for version in dependency.iter("version"):
                child["version"] = version.text
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
            for lib in project.iter("version"):
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
    test.get_dependency()
    print(test.get_maven_path())
    print(test.get_outlib())
    print(test.get_outheader())
    print(test.get_moduel_name())