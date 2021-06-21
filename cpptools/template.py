#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Lancer  2020-05-15 13:48:41


topcmake = \
"""\
# Auto CMakeLists.txt: frame  with  cppunit  use for lintcode/leetcode 
cmake_minimum_required(VERSION 3.7)

message("CMake version: " ${CMAKE_MAJOR_VERSION} .  ${CMAKE_MINOR_VERSION} . ${CMAKE_PATCH_VERSION})
if ( NOT PROJECT_SOURCE_DIR)
    PROJECT(%(prjname)s)
    MESSAGE(STATUS "## Making project " ${CMAKE_PROJECT_NAME})
    SET(ROOTPATH ${CMAKE_SOURCE_DIR})
endif()

add_subdirectory(src)

if (EXISTS ${CMAKE_SOURCE_DIR}/modsrc)
    file(GLOB MODSRC_SUB "modsrc/*")
    foreach(sd ${MODSRC_SUB})
        file(RELATIVE_PATH f ${CMAKE_SOURCE_DIR} ${sd})
        message(STATUS "Add modsrc sub directory: ${f}")
        add_subdirectory(${f})
    endforeach()
endif()
"""

src_leve_cmake = \
"""\
# cmvn tools auto generate CMakeLists.txt
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
SET( mname  %(prjname)s  )
SET( ROOTPATH ${CMAKE_SOURCE_DIR})

# defining common source variables
aux_source_directory(main   SRC )


#SET PROJECT OUTPUT DIR 
SET(EXECUTABLE_OUTPUT_PATH ${ROOTPATH}/bin/Debug)
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${ROOTPATH}/bin/Debug ) 


#PATH OR FILE ADD
IF ( EXISTS ${ROOTPATH}/cmake/common.cmake)
    include(${ROOTPATH}/cmake/common.cmake)
ENDIF()

include_directories(${ROOTPATH}/include)
include_directories(${ROOTPATH}/src)
include_directories(${ROOTPATH}/src/include)
#link_directories(${ROOTPATH}/lib/Windows)


#FUNCTION  
FUNCTION( target_ftest project_name  )
    IF (EXISTS ${ROOTPATH}/src/ftest)
        AUX_SOURCE_DIRECTORY(ftest  FTESTSRC )
        #link_directories(${ROOTPATH}/lib/Windows)
        ADD_EXECUTABLE( ftest_${project_name}  ${SRC}  ${FTESTSRC}  )
        #target_link_libraries(
        #   cppunit_${project_name}   
        #    
        #)
    ELSE()
        MESSAGE(STATUS " dir ftest not exist ")
    ENDIF()
ENDFUNCTION()

FUNCTION( target_cppunit project_name  )
    if (EXISTS ${ROOTPATH}/src/test_cppunit)
        AUX_SOURCE_DIRECTORY(test_cppunit  TESTSRC )
        add_definitions(-DCPPUNIT_TEST)
        link_directories(${ROOTPATH}/lib/Windows)
        add_executable( cppunit_${project_name}  ${SRC}  ${TESTSRC}  )
        target_link_libraries(
            cppunit_${project_name}   
            cppunit
        )
    else()
        message(STATUS " dir ftest not exist ")
    endif()
ENDFUNCTION()

FUNCTION( print_project_info )
    message("=============================================")
    message(" CMAKE_SYSTEM_NAME   : " ${CMAKE_SYSTEM_NAME} " " ${CMAKE_SYSTEM_PROCESSOR} )
    message(" CMAKE_C_COMPILER    : " ${CMAKE_C_COMPILER} )
    message(" CMAKE_CXX_COMPILER  : " ${CMAKE_CXX_COMPILER} )
    message(" CMAKE_ASM_COMPILER  : " ${CMAKE_ASM_COMPILER} )
    message(" CMAKE_C_FLAGS       : " ${CMAKE_C_FLAGS} )
    message(" CMAKE_CXX_FLAGS     : " ${CMAKE_CXX_FLAGS} )
    message(" CMAKE_C_FLAGS_INIT  : " ${CMAKE_C_FLAGS_INIT} )
    message(" CMAKE_CXX_FLAGS_INIT: " ${CMAKE_CXX_FLAGS_INIT} )
    message(" CMAKE_ASM_FLAGS_INIT: " ${CMAKE_ASM_FLAGS_INIT} )

    message(" EXECUTABLE_OUTPUT_PATH: " ${EXECUTABLE_OUTPUT_PATH} )
    message(" LIBRARY_OUTPUT_PATH   : " ${LIBRARY_OUTPUT_PATH} )
    message("=============================================")
ENDFUNCTION()

# Widows Visual Studio PROJECT
IF (CMAKE_SYSTEM_NAME MATCHES "Windows")
    MESSAGE(STATUS " current platform: Windows ")
    SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 

    #WINDOWS PC ADD CPPUINT FRAME
    target_cppunit( ${mname} )
# ARM MINGW PROJECT
ELSEIF (CMAKE_SYSTEM_NAME MATCHES "Linux") 
    MESSAGE( STATUS "current platform: Linux ")
    SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib/ARMCC) 
    SET(CMAKE_ASM_FLAGS_INIT  "--cpu Cortex-M3 -g --apcs=interwork --pd \\"__MICROLIB SETA 1\\" ")
    SET(CMAKE_C_FLAGS_INIT    "--c99 --gnu -c --cpu Cortex-M3 -D__MICROLIB -g -O0 --apcs=interwork --split_sections")
    SET(CMAKE_CXX_FLAGS_INIT  "${CMAKE_C_FLAGS_INIT}")
ELSE ()
    MESSAGE("=== other platform: ${CMAKE_SYSTEM_NAME} ")
ENDIF()

#TARGET OR LIB 
IF (SRC)
    ADD_LIBRARY( ${mname}  ${SRC} )  
    MESSAGE(STATUS "project src file: ")
    foreach(_var ${SRC})
        MESSAGE("   ${_var}")
    endforeach()
ENDIF(SRC)


target_ftest( ${mname} )
print_project_info()

"""

leetcode_cmake = \
"""\
# Auto CMakeLists.txt: use for lintcode/leetcode 
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

# top  project name
SET( mname  Solution  )

# defining common source variables
aux_source_directory(main   SRC )

SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 
SET(EXECUTABLE_OUTPUT_PATH ${root}/bin) 
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${ROOTPATH}/bin/Debug ) 
MESSAGE(STATUS "library_output_path   : " ${LIBRARY_OUTPUT_PATH} )
MESSAGE(STATUS "executable_output_path: " ${EXECUTABLE_OUTPUT_PATH} )
MESSAGE(STATUS "cmake_runtime_output_directory_debug: " ${CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG} )



message("==================== cppbuilder init start: ====================")
if(SRC)
    ADD_LIBRARY( ${mname}_static  STATIC  ${SRC} )   
    #ADD_LIBRARY( ${mname} SHARED  ${SRC} )
    add_executable( t_${mname}  ${SRC} )
endif(SRC)

message("==================== cppbuilder   init  end ====================")
"""

cppunit_testmain = \
"""
#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>

#ifdef  CPPUNIT_TEST
void  main()
{
    CppUnit::TextUi::TestRunner runner;
    CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry("cppunit_test_all");
    runner.addTest( registry.makeTest() );
    runner.run();
}
#endif
"""

cppunit_testfile = \
"""\
#include <cppunit/extensions/HelperMacros.h>
#include "publicbase.h"
    
    
extern "C" 
{
    extern const module_info_t ver_%(prjname)s; 
}
#define CPPUNIT_EASSERT(a,b) CPPUNIT_ASSERT_EQUAL((int)a, (int)b)

class  %(prjname)s_test : public CPPUNIT_NS::TestFixture
{
    CPPUNIT_TEST_SUITE(%(prjname)s_test);
    CPPUNIT_TEST(%(prjname)s_test_ver            );
    CPPUNIT_TEST_SUITE_END();

public:
    %(prjname)s_test();
    virtual ~%(prjname)s_test();
    virtual void setUp();
    virtual void tearDown();
    void %(prjname)s_test_ver ();
};
    
%(prjname)s_test::%(prjname)s_test()
{
}
%(prjname)s_test::~%(prjname)s_test()
{
}

void %(prjname)s_test::setUp()
{
}

void %(prjname)s_test::tearDown()
{
}

void %(prjname)s_test::%(prjname)s_test_ver()
{

    CPPUNIT_EASSERT( 0, ver_%(prjname)s.major ); 
    CPPUNIT_EASSERT( 0, ver_%(prjname)s.minor ); 
    CPPUNIT_EASSERT( 1, ver_%(prjname)s.patch ); 
}

//将TestSuite注册到一个名为alltest的TestSuite中
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(  %(prjname)s_test,"cppunit_test_all");
"""

cppfile_template = \
"""
#include "publicbase.h"


"""

ver_module_template = \
"""
#include "publicbase.h"

const module_info_t ver_%(prjname)s=
{
/*- name */    "%(prjname)s",
/*- time */    __TIME__,
/*- major*/    0,
/*- minor*/    0,
/*- patch*/    1,
};

"""


cppfile_template_lintcode = \
"""\
#include <stdio.h>



int  main(int argc,char **argv)
{
    return 0 ;
}

"""

hhp_template = \
"""\
#ifndef  __%(prjname)s_H__
#define  __%(prjname)s_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "publicbase.h"


//extern  int  myadd(int x, int y) ;



#ifdef __cplusplus
}
#endif

#endif



"""

readme_template = \
"""\
##  Auto create  readme.md



"""

pom_template = \
"""\
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <groupId>%(groupId)s</groupId>
    <artifactId>%(prjname)s</artifactId>
    <version>0.0.1</version>
    <lib>%(prjname)s</lib>
    <header>%(prjname)s.h</header>

    <dependencies>
        <!-- use only for utest  -->
        <dependency><artifactId>com.utest.cppunit</artifactId></dependency>
        <!-- add child moduel info, tools will auto pull .lib and .h files -->

    </dependencies>
</project>
"""

armcmake_template = \
'''
###########################################
#   armcc cmake cross toolchain file      #
###########################################
# minimum  cmake  version  
cmake_minimum_required(VERSION 3.7)

SET(CMAKE_SYSTEM_NAME Linux)
SET(CMAKE_SYSTEM_PROCESSOR arm)

SET(ARMCC_ROOT  "D:/myprogram/keil5/ARM/ARMCC")
SET(CMAKE_C_COMPILER  ${ARMCC_ROOT}/bin/armcc.exe)
SET(CMAKE_CXX_COMPILER  ${CMAKE_C_COMPILER})
SET(CMAKE_ASM_COMPILER ${ARMCC_ROOT}/bin/armasm.exe)
SET(CMAKE_LINKER ${ARMCC_ROOT}/bin/armlink.exe )
SET(CMAKE_AR ${ARMCC_ROOT}/bin/armar.exe)
SET(INIT_CP_FLAGS "--apcs=interwork -c --cpu=cortex-a9 -O0 --debug -DVFP_DREG=32 --fpu=vfpv3 --c90 -g")

'''

common_template = \
'''
#  common cmake file: all define  functions  

function(set_output_path)
    #set(CMAKE_SYSTEM_NAME ${platform} )
    IF (CMAKE_SYSTEM_NAME MATCHES "Windows")
        MESSAGE("=== current platform: Windows ")
        SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib) 
        MESSAGE(STATUS "library_output_path   : " ${LIBRARY_OUTPUT_PATH} )
    ELSEIF (CMAKE_SYSTEM_NAME MATCHES "Linux")
        MESSAGE("=== current platform: Linux ")
        SET(LIBRARY_OUTPUT_PATH ${ROOTPATH}/lib/ARMCC) 
        MESSAGE(STATUS "library_output_path   : " ${LIBRARY_OUTPUT_PATH} )
    ELSE ()
        MESSAGE("=== other platform: ${CMAKE_SYSTEM_NAME} ")
    ENDIF()
endfunction(set_output_path)

'''