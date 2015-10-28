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


    def testParseCmd_All_OK(self):
        argString = '-b 40 -t 60 -l 5 -r 15 --ci 10 --ce 50 --ca 100 --mi 6400 --mn GER --fi 1441 --nc --no-contours -i input.txt'
        self.creator=MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()
        self.assertEqual(40,          cmdArgs.bottom,    'bottom was not parsed properly')
        self.assertEqual(60,          cmdArgs.top,       'top was not parsed properly')
        self.assertEqual(5,           cmdArgs.left,      'left was not parsed properly')
        self.assertEqual(15,          cmdArgs.right,     'right was not parsed properly')
        
        self.assertEqual(10,          cmdArgs.cstepmin,  'minimum contour step was not parsed properly')
        self.assertEqual(50,          cmdArgs.cstepmed,  'medium contour step was not parsed properly')
        self.assertEqual(100,         cmdArgs.cstepmax,  'maximum contour step was not parsed properly')
        
        self.assertEqual(6400,        cmdArgs.mapid,     'mapid was not parsed properly')
        self.assertEqual("GER",       cmdArgs.mapname,   'mapname was not parsed properly')
        
        self.assertEqual(1441,        cmdArgs.famid,     'family id was not parsed properly')
        self.assertEqual(2441,        cmdArgs.cminid,    'minor contour map family id was not parsed properly')
        self.assertEqual(2443,        cmdArgs.cmaxid,    'major contour map family id was not parsed properly')
        
        self.assertEqual(True,        cmdArgs.nocontours, 'nocontous flag was not parsed properly')
           
        self.assertEqual('input.txt', cmdArgs.inputfile, 'inputfile was not parsed properly')
        


if __name__ == "__main__":
    unittest.main()