# -*- encoding: utf-8 -*-
#@File    : util.py.py
#@Time    : 2020/6/20 10:19
#@Author  : Lancer

import  os,sys
import  shutil,binascii


def  create_file(filename, content,encoding_str="utf-8"):
    '''
    创建文件 默认UTF-8
    filename: 文件名(含路径)
    content:  文件内容
    '''
    old_path = os.getcwd()
    name = filename.split("\\")[-1]
    filepath = "\\".join(filename.split("\\")[0:-1:])
    if  filepath:
        if False == os.path.exists(filepath):
            os.makedirs(filepath)
        os.chdir(filepath)
    with  open(name, mode="w", encoding=encoding_str) as file:
        file.write(content)
        file.close()
    os.chdir(old_path)
    print("create file success: [ %s ] "%(filename))

def open_file(filename):
    try:
        with  open(filename, mode="r", encoding='utf-8') as file:
            return file.read()
    except  UnicodeDecodeError:
        with  open(filename, mode="r", encoding='gbk') as file:
            return file.read()
    except  IOError:
        print("cannot find file: %s "%(filename))

def  copy_file(srcfile, dstfile):
    dir = "\\".join(dstfile.split("\\")[0:-1:] )
    if not os.path.exists(dir):
        os.makedirs("\\".join(dstfile.split("\\")[0:-1:]))
    try:
        if not os.path.exists(srcfile):
            print("srcfile not exist: %s"%(srcfile))
        shutil.copy2(srcfile,dstfile)
    except FileNotFoundError:
        print("copy fail: %s to  %s"%(srcfile,dstfile))

def is_same_file(filename, fulldstname):
    """
     @brief is_same_file 首先判断修改大小，再判断修改时间，若都一致，初步判断一致
    """
    ret = False
    if os.path.exists(fulldstname):
        curstat = os.stat(filename)
        oldstat = os.stat(fulldstname)
        if (curstat.st_size == oldstat.st_size
            and int(curstat.st_mtime*1000) == int(oldstat.st_mtime*1000)
           ):
            ret = True
    return ret

def make_dirs(new_dir,topath=False):
    # r'project\debug\test'
    if not os.path.exists(new_dir):
        try:
            os.makedirs(new_dir)
            print("new dir %s success"%(new_dir))
        except Exception as e:
            print(e)
        finally:
            if topath == True:
                os.chdir(new_dir) 
        
def run_cmd( cmds, src_path="", back_path="" ):
    if src_path:
        try:
            os.chdir(src_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s"%(src_path))
        finally:
            os.chdir(os.getcwd())
    if isinstance(cmds,str):
        os.system(cmds)
    elif isinstance(cmds,list) or isinstance(cmds,tuple):
        for cmd in cmds:
            os.system(cmd)
    elif isinstance(cmds,dict):
        for key,value in cmds.items():
            try:
                key(value)
            except Exception as e :
                #print("=== function: %s cmd: %s "%(str(key),str(value) ))  
                print("=== err: ", e)      
    else:
        print("=== unexpect  input data type")
    if back_path:
        try:
            os.chdir(back_path)
        except FileNotFoundError as e:
            print("=== dir not exsist: %s  "%(back_path))
        finally:
            os.chdir(os.getcwd())

if __name__ == '__main__':
    pass
    # create_file(r"src\ftest\ftest.cpp","TTTTTT")
    # create_file(r"tttest.cpp", "TTTTTT")
    #print(open_file("tttest.cpp"))
    #copy_file("src\\0.0.1_pom.xml",r'src\0.0.34_pom.xml')