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

from SplitterCommand import SplitterCommand

sys.path.append('../../src/python')

class SplitterCommand_test(unittest.TestCase):


    def setUp(self):
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__splitterTool = os.path.join(self.__toolsDir, "splitter/lib/splitter.jar")
        self.__splitterCmd = SplitterCommand()
        logging.basicConfig(level=logging.DEBUG)


    def tearDown(self):
        pass


    def testsplitAreaIntoTiles(self):
        cmdstr = self.__splitterCmd.splitAreaIntoTiles()


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))