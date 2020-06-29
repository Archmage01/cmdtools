
##  自用python命令行工具

###  1 工具简介
- 本工具基于python3开发, 自用于创建模板文件,节省重复时间。
- 支持cpp/c/java 命令行编译
    - 1 cpp/c 工程需要提前安装好cmake 及Visual Studio 2015(其他版本也行)
    - 2 java  工程需提前安装 maven 及java jdk等(完全依赖mvn命令行)

###  2 使用介绍

```
version: 1.0.0   data: 2020-05-08  author: lancer
cmdtools:
    
    [-c ib  ]  :  smb init &&　smb  build 
    [-c ibu ]  :  smb init &&　smb  build  &&  smb  utest
    [-c ixl ]  :  smb init &&　smb  xbinfo armcc  &&  smb lmake
```

### 3 Maven 常用命令介绍

| 描述 | 命令 |
|:--|:--|
| 编译源代码  | mvn compile |
| 编译测试代码 | mvn test-compile |
| 运行测试 | mvn test  |
| 打包 |mvn package   |
| 在本地Repository中安装jar |mvn install    |
| 清除产生的项目 | mvn clean |