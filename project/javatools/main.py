#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-08 08:45:33

import  os,re,sys
import  getopt
import  help
import  java_mvn
import  cpp_project

class  Main(object):

    def __init__(self):
        self.cmd_dict = {
            "ib": help.cmd_header_ib ,
            "ibu": help.cmd_header_ibu ,
            "ixl": help.cmd_header_ixl ,
        }


    def main(self):
        try:
            apts, msgs = getopt.getopt(sys.argv[1:],shortopts="vhjo:c:",longopts = ["help","version","leetcode=","cpp"] )
            # print("apts",apts, end=" " )
            # print(" msgs",msgs )
            for opt , msg in apts:
                if opt in ("-c"):
                    if msg in self.cmd_dict.keys():
                        self.cmd_dict[msg]()
                elif  opt in ("-j"):
                    java_cmd = java_mvn.JavaMvn(msgs)
                elif  opt in ("-v","-h","--version","--help"):
                    help.print_help()
                elif opt in ("--cpp"):
                    cpp_cmd = cpp_project.CppProject(msgs)

        except getopt.GetoptError:
            help.print_help()




if __name__ == "__main__":
    test =  Main()
    test.main()
