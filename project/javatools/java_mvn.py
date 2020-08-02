#!/usr/bin/env python3 
# -*- coding:utf-8 -*-
# Author: yang.gan  2020-04-12 21:55:51

import  os
import  sys
import  re



class  JavaMvn(object):
    def __init__(self, args ):
        self.cmd_dict = {
            "build": self.mvn_build,
            "test" : self.mvn_test ,
        }
        self.root_path = os.getcwd()
        self.praser_javaproject_cmd(args)
        
    
    def  praser_javaproject_cmd(self, args ):
        if len(args) == 1:
            if args[0] in ("build","test"):
                self.cmd_dict[args[0]]()
            else:
                self.run_class(args[0])
        else:
            # create project
            try:
                if args[0] == "create" and len(args)>1:
                    args = args[1].split(".")
                    artifactId = args[-1]
                    groupId = ""
                    for i in range(len(args)-1):
                        groupId += args[i]+"."
                    groupId = groupId[0:len(groupId)-1:]
                    self.create_mvn_project( groupId,artifactId )
            except Exception as e :
                print(e)
             
    def create_mvn_project(self, groupId, artifactId ):
        total_cmd = "mvn archetype:generate -DgroupId=%s -DartifactId=%s  -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false"%(groupId,artifactId)
        print("\ncreate:",total_cmd)
        os.system(total_cmd)
        os.chdir(artifactId)


    def mvn_build(self):
        os.system("mvn compile")

    def mvn_test(self):
        os.system("mvn test")

    def run_class(self,class_name):
        pack_name = ""
        if os.path.exists("pom.xml"):
            try:
                file = open("pom.xml",encoding="utf-8",mode="r")
                lines = file.readlines()
                for line in  lines:
                    line = line.strip()
                    if line.startswith("<groupId>") and  line.endswith("</groupId>"):
                        pack_name =  line.replace("<groupId>","").replace("</groupId>","")
                        break
                file.close()
                #self.root_path
                cu_dir = self.root_path+r'\target\classes'
                os.chdir(cu_dir)
                pack_name = "java " + pack_name+".%s"%(class_name)
                os.system(pack_name)
                os.chdir(self.root_path)
            except Exception as e:
                print(e)
        else:
            print("this path not exsist pom.xml")



if __name__ == "__main__":
    pass
    
