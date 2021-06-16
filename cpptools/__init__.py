#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
version 1.0.0 
    支持基本功能:
    1. 支持自动创建c/cpp 项目，支持编译等
    2. 支持库管理, 安装库文件 头文件安装
    3. 支持拉取子模块库文件头文件(windows平台,支持指定版本文件编译)
version 1.0.1
    1 支持单元测试框架，需要首先安装模块com.utest.cppunit, 安装库文件,头文件脚本copy到标准头文件路径
    2 支持模块版本号
    3 支持命令更新模块版本号
version 1.0.2
    1 支持同一模块放出多个头文件
    2 支持输出头文件目录嵌套
version 1.0.3
    1  支持校验版本号: pom.xml  单元测试  版本源码 是否一致
    2  模板生成头文件, 单元测试文件
version 1.0.4
    1 支持交叉编译ARM, 需要安装keil和mingw(mingw工程 arm编译工具链)
    2 arm平台生成静态库.a 和 烧入bin文件(cmake编译链中指定arm平台参数等)        
    3 支持命令 .elf 生成 .bin文件
    
version 2.0.0
    待添加
    

'''