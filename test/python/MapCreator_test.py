'''
Created on 25.10.2015

@author: mevo
'''
import unittest
import shlex
from MapCreator import MapCreator


class Test(unittest.TestCase):


    def setUp(self):
        argString = '-b 10 -t 11 -l 12 -r 13 -i input.txt'
        self.creator=MapCreator(shlex.split(argString))


    def tearDown(self):
        pass


    def testParseCmd(self):
        argString = '-b 10 -t 11 -l 12 -r 13 -i input.txt'
        cmdArgs = self.creator.getArgs()
        self.assertEqual(10, cmdArgs.bottom, 'bottom was not parsed properly')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()