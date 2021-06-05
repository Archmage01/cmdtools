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
        self.assertEqual(test.groupid,    ['lrts','ws'])
        self.assertEqual(test.artifactId, ['protocol'] )
        self.assertEqual(test.version,    ['2.2.5']    )
        self.assertEqual(test.header_prefix,['app','ws'])
        self.assertEqual(test.header,      ['protocol.h'])
        self.assertEqual(test.lib,         ['protocol'])
        dp = {
            "lrts.ws.interface":None,
            "unifw.plat.ssimp": None,
            "unifw.base.codebase":None,
            "unifw.base.b2v":    None,
            "unifw.base.ring":None,
            "lrts.ws.wspub":None,
        }
        self.assertEqual(test.get_dependencies(), dp )




if __name__ == '__main__':
    unittest.main()
