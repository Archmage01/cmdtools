#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys,os
sys.path.append('../cpptools')
from pom import *
from pub import *

class MyTestCase(unittest.TestCase):
    def test_get_moduel_base_info(self):
        test = Pom('../resources/pom.xml')
        print(test.header)
        self.assertEqual(test.groupid,    ['lrts','ws'])
        self.assertEqual(test.artifactId, ['protocol'] )
        self.assertEqual(test.version,    ['2.2.5']    )
        self.assertEqual(test.header_prefix,['app','ws'])
        self.assertEqual(test.header,      ['protocol.h',"protocol_test.h"])
        self.assertEqual(test.lib,         ['protocol'])
        dp = {
            "unifw.base.b2v":    None,
            "unifw.base.ring":None,
            "lrts.ws.wspub":None,
        }
        
        self.assertEqual(test.get_dependencies(), {} )




if __name__ == '__main__':
    unittest.main()
