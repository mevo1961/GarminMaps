'''
Created on 31.01.2016

@author: mevo
'''
import logging
import os
import sys
import time
import unittest
import xmlrunner

sys.path.append('../../src/python')

from SplitterCommand import SplitterCommand


class SplitterCommand_test(unittest.TestCase):


    def setUp(self):
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__splitterTool = os.path.join(self.__toolsDir, "splitter/splitter.jar")
        self.__splitterCmd = SplitterCommand()
        self.__dataDir = os.path.abspath("../../data") + "/"
        logging.basicConfig(level=logging.DEBUG)


    def tearDown(self):
        pass


    def testsplitAreaIntoTiles(self):
        cmdstr = self.__splitterCmd.splitAreaIntoTiles(self.__dataDir + "temp.osm", self.__dataDir, "6400")
        expectedStr = "java -Xmx2000M -jar " + self.__splitterTool + \
                      " --mapid=64000001 --max-nodes=800000 --max-areas=20 --output-dir=" + self.__dataDir + " " +self.__dataDir + "temp.osm"
        self.assertEqual(expectedStr, cmdstr,  
                            'SplitterCmd was not composed properly, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))