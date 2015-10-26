'''
Created on 25.10.2015

@author: mevo
'''
import unittest
import shlex
from MapCreator import MapCreator


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testParseCmd_OK(self):
        argString = '-b 10 -t 11 -l 12 -r 13 -i input.txt'
        self.creator=MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()
        self.assertEqual(10,          cmdArgs.bottom,    'bottom was not parsed properly')
        self.assertEqual(11,          cmdArgs.top,       'top was not parsed properly')
        self.assertEqual(12,          cmdArgs.left,      'left was not parsed properly')
        self.assertEqual(13,          cmdArgs.right,     'right was not parsed properly')
        self.assertEqual('input.txt', cmdArgs.inputfile, 'inputfile was not parsed properly')


if __name__ == "__main__":
    unittest.main()