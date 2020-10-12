# -*- encoding: utf-8 -*-
#@File    : tools.py
#@Time    : 2020/10/12 15:03
#@Author  : Lancer

import  os,re,sys
import  getopt,codecs


'''
工具转化文件编码格式 目前支持: UTF-8 to gbk   and  gbk to utf-8
'''

def get_file(type=None):
    ret = []
    for root, dirs, files in os.walk(os.getcwd(),topdown=True):
        for name in files:
            if name.split(".")[-1] == type and type is not None:
                ret.append(os.path.join(root, name))
            if not type:
                ret.append(os.path.join(root, name))
    return ret


def ReadFile(filePath, encoding="utf-8"):
    with codecs.open(filePath, "r", encoding) as f:
        return f.read()


def WriteFile(filePath, u, encoding="gbk"):
    with codecs.open(filePath, "w", encoding) as f:
        f.write(u)


def UTF8_2_GBK(src, dst):
    content = ReadFile(src, encoding="utf-8")
    WriteFile(dst, content, encoding="gbk")

def GBK_2_UFT8(src, dst):
    content = ReadFile(src, encoding="gbk")
    WriteFile(dst, content, encoding="utf-8")

def  convert(files,src='gbk',dst='utf-8'):
    rootpath = os.getcwd()
    for file in files:
        try:
            if src=="gbk":
                GBK_2_UFT8(file,file)
            else:
                UTF8_2_GBK(file, file)

        except Exception as e:
            print("err", file," ",e )



if __name__ == '__main__':
    try:
        apts, msgs = getopt.getopt(sys.argv[1:], shortopts="vh", longopts=["help", "version"])
        # print(apts)
        # print(msgs)
        for apt, _ in apts:
            if apt in ("-v", "--version"):
                print("\n version: 1.0.0  time:2020-10-20 author:Lancer")
            elif apt in ("-h", "--help"):
                print("工具转化文件编码格式 目前只支持UTF-8 转gbk  和 gbk 转UTF-8 ")
        if not apts:
            if msgs[0] == "togbk":
                print("转为gbk",len(msgs) )
                filelist = []
                if len(msgs)>1:
                    filelist = get_file(msgs[1])
                else:
                    filelist = get_file()
                convert(filelist,src='utf-8',dst='gbk')
            elif msgs[0] == "toutf8":
                print("转为utf-8")
                filelist = []
                if len(msgs)>1:
                    filelist = get_file(msgs[1])
                else:
                    filelist = get_file()
                convert(filelist, src='gbk', dst='utf-8')
            else:
                print("CMD ERR")
    except getopt.GetoptError:
        print("cmd err please read help info : -h  gettools use info ")