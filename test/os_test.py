#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest
import sys,os,time

class MyTestCase(unittest.TestCase):
    def  test_expanduser(self):
        print("当前用户目录:", os.path.expanduser('~'))
        self.assertEqual(True, True)

    def test_getmtime(self):
        print("返回path的最后修改时间", os.path.getmtime(os.getcwd()),end=" ")
        local_time = time.localtime(os.path.getmtime(os.getcwd()))
        #print(local_time)
        timestr = time.strftime("%Y-%m-%d %H:%M:%S",local_time )
        print(timestr)

    def test_basename(self):
        # 如果path以／或\结尾，那么就会返回空值
        # 返回path最后的文件名
        self.assertEqual(os.path.basename("top/demo/test/"), "")
        self.assertEqual(os.path.basename("top/demo/test"), "test")
        self.assertEqual(os.path.basename( os.getcwd()+"\\test.cpp"), "test.cpp")

    def test_str_01(self):
        test01 = "D:/test/test1/last/test.cpp"
        test02 = "D:/test/"
        print("============= ", test01.strip(test02))
        print(test01.split(test02))


if __name__ == '__main__':
    unittest.main()