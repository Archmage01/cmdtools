#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33
import os,sys,re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class  ParsePom(object):
    def __init__(self,pomfile):
        self.tree = ET.parse("pom.xml")
        self.root = self.tree.getroot()

    def get_pom_text(self, tag):
        ret = []
        if  isinstance(tag,str):
            for tagtext in  self.root.iter('%s'%(tag)):
                ret.append(tagtext.text)
                #print(dependency.tag)
                #print(dependency.attrib)
        elif isinstance(tag,list):
            for v in tag:
                for tagtext in  self.root.iter('%s'%(v)):
                    ret.append(tagtext.text)
        return ret

    def get_dependency(self):
        return self.get_pom_text("dependency")

    def get_maven_path(self):
        return self.get_pom_text("groupId")

    def get_out_lib(self):
        return self.get_pom_text("lib")

    def get_out_lib_version(self):
        return self.get_pom_text("version")
    
    def get_out_head(self):
        return self.get_pom_text("header")
