# 修订记录

- version 1.0.0 

    支持基本功能:
    - 1. 支持自动创建c/cpp 项目，支持编译等
    - 2. 支持库管理, 安装库文件 头文件安装
    - 3. 支持拉取子模块库文件头文件(windows平台,支持指定版本文件编译)
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
- version 1.0.4
    - 1 支持交叉编译ARM, 需要安装keil和mingw(mingw工程 arm编译工具链)
    - 2 arm平台生成静态库.a 和 烧入bin文件(cmake编译链中指定arm平台参数等)        
    - 3 支持命令 .elf 生成 .bin文件
- version 2.0.0
    - 1 支持STM32F103VET6(自己玩的野火指南板)ARM集成开发
    - 2 不同芯片需要变更的地方：
        - 2.1  需要手动复制start文件
        - 2.2  STM32标准库可以源码集成(手动修改cmake),或者将源码编译为静态库pom依赖
        - 2.3  需要修改cmake中编译选项根据芯片不同
    - 3 本工具将stm32库代码和应用代码分层, 让我们只需要关注应用层逻辑代码
      用vscode等用户界面友好的编辑器,而不需要用keil,模板化工程目录
    


# 工具简介

```
This tool is modeled on MVN for C/C++ project, need install cmake tools/ Visual Studio/ keil / mingw
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
    verify                  verify version number consistency 

    arminit                 Generators MinGW Makefiles 
    armbuild                keil  build  project 
    arminstall              Install the packaged project to the local warehouse for use by other projects(arm)
    elf2bin                 from  change .elf to .bin  .hex and so on 
options:
    -v, --version           Displays the tool version number and modification time
    -h, --help              Display help information for users to use tools


```