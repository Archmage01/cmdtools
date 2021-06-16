# 修订记录

- version 1.0.0
    - 0 支持基本功能:
    - 1 支持自动创建c/cpp 项目，支持编译等
    - 2 支持库管理, 安装库文件 头文件安装
    - 3 支持拉取子模块库文件头文件(windows平台,支持指定版本文件编译)
- version 1.0.1
    - 1 支持单元测试框架，需要首先安装模块com.utest.cppunit, 安装库文件,头文件脚本copy到标准头文件路径
    - 2 支持模块版本号
    - 3 支持命令更新模块版本号
- version 1.0.2
    - 1 支持同一模块放出多个头文件
    - 2 支持输出头文件目录嵌套
- version 1.0.3
    - 1  支持校验版本号: pom.xml  单元测试  版本源码 是否一致
    - 2  模板生成头文件, 单元测试文件

# 工具简介

```
This tool is modeled on MVN for C/C++ project, need install cmake tools/ Visual Studio
usage: cmvn cmds [options] [optioninfo] 

cmds:
    create  projectinfo     projectinfo is Unique identification, for example: com.leetcode.demo
    init                    run at project root path prepare for compile project 
                            to get dependencies moduel files like  .h or .lib
    build                   compile this project, generate executable file or .lib 
    install                 Install the packaged project to the local warehouse for use by other projects
    utest                   Run the tests using the appropriate unit testing framework, such as cppunit
    ftest                   Run the tests in dir ftest, like integration testing
    clean                   Remove all files generated from the last build
    update destversion      destversion is version number to be upgraded, for example: 1.0.0
    deploy                  Copy the final project package to the remote warehouse for sharing with other developers and projects
    generate fileinfo       generate file, tools will analysis fileinfo by rules output template file

options:
    -v, --version           Displays the tool version number and modification time
    -h, --help              Display help information for users to use tools



```