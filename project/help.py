#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33

import os

helpinfo = \
'''
    version: 1.0.2   data: 2020-05-20  author: lancer
    cmdtools:
        
        [-c ib  ]  :  smb init &&　smb  build 
        [-c ibu ]  :  smb init &&　smb  build  &&  smb  utest
        [-c ixl ]  :  smb init &&　smb  xbinfo armcc  &&  smb  lmake
    
    maven java:
        [-j create com.lancer.demo ]:   -DgroupId=com.lancer -DartifactId=demo  maven-archetype-quickstart
        [-j build                  ]:   mvn compile
        [-j test                   ]:   mvn test
        [-j className              ]:   
    cpp tools:
        [-- cpp  create leetcode     ]   easy    project
        [-- cpp  create project name ]   create  project  need  cppunit  
        [-- cpp  init                ]   need  cmake version >= 3.7
        [-- cpp  build               ]   build  and  make  target
        [-- cpp  utest               ]   cppunit  result  or  target.exe 

'''


def  print_help():
    print(helpinfo)

    

def  cmd_header_ib():
    os.system("smb init && smb  build ")

def  cmd_header_ibu():
    os.system("smb init && smb  build && smb  utest ")

def  cmd_header_ixl():
    os.system("smb init &&　smb  xbinfo armcc  &&  smb  lmake ")

