'''
Created on 25.10.2015

@author: mevo
'''
import unittest
import shlex
import sys
import xmlrunner

sys.path.append('../../src/python')

from MapCreator import MapCreator


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testParseCmdLine_All_OK(self):
        argString = '-b 40 -t 60 -l 5 -r 15 --ci 20 --ce 40 --ca 80 --mi 6666 --mn FRA --fi 1111 --cid 2222 --cad 3333 --nc --no-contours -i input.txt'
        self.creator=MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()

        self.assertEqual(40,          cmdArgs.bottom,     'bottom was not parsed properly')
        self.assertEqual(60,          cmdArgs.top,        'top was not parsed properly')
        self.assertEqual(5,           cmdArgs.left,       'left was not parsed properly')
        self.assertEqual(15,          cmdArgs.right,      'right was not parsed properly')
        
        self.assertEqual(20,          cmdArgs.cstepmin,   'minimum contour step was not parsed properly')
        self.assertEqual(40,          cmdArgs.cstepmed,   'medium contour step was not parsed properly')
        self.assertEqual(80,         cmdArgs.cstepmax,   'maximum contour step was not parsed properly')
        
        self.assertEqual(6666,        cmdArgs.mapid,      'mapid was not parsed properly')
        self.assertEqual("FRA",       cmdArgs.mapname,    'mapname was not parsed properly')
        
        self.assertEqual(1111,        cmdArgs.famid,      'family id was not parsed properly')
        self.assertEqual(2222,        cmdArgs.cminid,     'minor contour map family id was not parsed properly')
        self.assertEqual(3333,        cmdArgs.cmaxid,     'major contour map family id was not parsed properly')
        
        self.assertEqual(True,        cmdArgs.nocontours, 'nocontours flag was not parsed properly')
           
        self.assertEqual('input.txt', cmdArgs.inputfile,  'inputfile was not parsed properly')
        
    
    def testParseCmdLine_Defaults(self):
        argString = '-i input.txt'
        self.creator = MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()

        self.assertEqual(47.2,        cmdArgs.bottom,     'bottom was not parsed properly')
        self.assertEqual(55.2,        cmdArgs.top,        'top was not parsed properly')
        self.assertEqual(5.7,         cmdArgs.left,       'left was not parsed properly')
        self.assertEqual(15.1,        cmdArgs.right,      'right was not parsed properly')
        
        self.assertEqual(10,          cmdArgs.cstepmin,   'minimum contour step was not parsed properly')
        self.assertEqual(50,          cmdArgs.cstepmed,   'medium contour step was not parsed properly')
        self.assertEqual(100,         cmdArgs.cstepmax,   'maximum contour step was not parsed properly')
        
        self.assertEqual(6400,        cmdArgs.mapid,      'mapid was not parsed properly')
        self.assertEqual("GER",       cmdArgs.mapname,    'mapname was not parsed properly')
        
        self.assertEqual(1441,        cmdArgs.famid,      'family id was not parsed properly')
        self.assertEqual(2441,        cmdArgs.cminid,     'minor contour map family id was not parsed properly')
        self.assertEqual(2443,        cmdArgs.cmaxid,     'major contour map family id was not parsed properly')
        
        self.assertEqual(False,       cmdArgs.nocontours, 'nocontours flag was not parsed properly')
           
        self.assertEqual('input.txt', cmdArgs.inputfile,  'inputfile was not parsed properly')
        
    # def testCutOutMapData(self):
        # argString = '-i input.txt'
        # self.creator =M apCreator(shlex.split(argString))
        # self.creator.cutOutMapData()
        # pass
        


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    # unittest.main()
