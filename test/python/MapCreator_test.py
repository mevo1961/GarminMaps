'''
Created on 25.10.2015

@author: mevo
'''
import unittest
import shlex
import sys
import time
import os
import xmlrunner
import logging

sys.path.append('../../src/python')

from MapCreator import MapCreator


class Test_MapCreator(unittest.TestCase):


    def setUp(self):
        self.maxDiff = None
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
        self.__dataDir = os.path.abspath("../../data") + "/"
        logging.basicConfig(level=logging.DEBUG)


    def tearDown(self):
        pass


    def testParseCmdLine_All_OK(self):
        argString = '-b 40 -t 60 -l 5 -r 15 -p germany.poly --ci 20 --ce 40 --ca 80 --mi 6666 --mn FRA --fi 1111 --cid 2222 --cad 3333 --nc --no-contours -i input.osm'
        self.creator=MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()

        self.assertEqual(40,             cmdArgs.bottom,     'bottom was not parsed properly')
        self.assertEqual(60,             cmdArgs.top,        'top was not parsed properly')
        self.assertEqual(5,              cmdArgs.left,       'left was not parsed properly')
        self.assertEqual(15,             cmdArgs.right,      'right was not parsed properly')
        
        self.assertEqual('germany.poly', cmdArgs.poly,       'polygon file was not parsed properly')
        
        self.assertEqual(20,             cmdArgs.cstepmin,   'minimum contour step was not parsed properly')
        self.assertEqual(40,             cmdArgs.cstepmed,   'medium contour step was not parsed properly')
        self.assertEqual(80,             cmdArgs.cstepmax,   'maximum contour step was not parsed properly')
        
        self.assertEqual(6666,           cmdArgs.mapid,      'mapid was not parsed properly')
        self.assertEqual("FRA",          cmdArgs.mapname,    'mapname was not parsed properly')
        
        self.assertEqual(1111,           cmdArgs.famid,      'family id was not parsed properly')
        self.assertEqual(2222,           cmdArgs.cminid,     'minor contour map family id was not parsed properly')
        self.assertEqual(3333,           cmdArgs.cmaxid,     'major contour map family id was not parsed properly')
        
        self.assertEqual(True,           cmdArgs.nocontours, 'nocontours flag was not parsed properly')
           
        self.assertEqual('input.osm',    cmdArgs.inputfile,  'inputfile was not parsed properly')
        
    
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
        
    def testCutMapDataWithPolygon(self):
        argString = '-i ' + self.__dataDir + 'germany.osm -p ' + self.__dataDir + 'germany.poly'
        outfile = self.__dataDir + "temp.osm"
        self.creator = MapCreator(shlex.split(argString), test=True)
        result = self.creator.cutMapDataWithPolygon()
        expectedStr = self.__osmosisTool + ' --read-xml file="' + self.__dataDir + 'germany.osm" --bounding-polygon file="' + self.__dataDir + 'germany.poly" completeWays=no --write-xml file="' + outfile + '"'
        self.assertEqual(expectedStr, result, 'unexpected command for cutting mapdata with polygon, \nexpected: %s,\nbut was:  %s' % (expectedStr, result))
        
            
    def testCutMapDataWithBoundingBox(self):
        argString = '-i ' + self.__dataDir + 'germany.osm -t 48.5 -l 9.8 -b 48.4 -r 10.0'
        outfile = self.__dataDir + "temp.osm"
        self.creator = MapCreator(shlex.split(argString), test=True)
        result = self.creator.cutMapDataWithBoundingBox()
        expectedStr = self.__osmosisTool + ' --read-xml file="' + self.__dataDir + 'germany.osm" --bounding-box top=48.5 left=9.8 bottom=48.4 right=10.0 completeWays=no --write-xml file="' + outfile + '"'
        self.assertEqual(expectedStr, result, 'unexpected command for cutting mapdata with polygon, \nexpected: %s,\nbut was:  %s' % (expectedStr, result))
    
    def testIsDataFileOk(self):
        argString = '-i input.txt'
        self.creator = MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()
        # file does not exist, must throw exception
        with self.assertRaises(IOError):
            self.creator.isDataFileOk(cmdArgs.inputfile)
        # the following infile must be accepted 
        infile = self.__dataDir + 'germany.osm'
        self.assertTrue(self.creator.isDataFileOk(infile), "%s is a not valid inputfile" % infile)
        # the following infile must not be accepted
        infile = self.__dataDir + 'mapdata.txt'
        self.assertFalse(self.creator.isDataFileOk(infile), "%s is a valid inputfile" % infile)
    
    
    def testIsPolyFileOk(self):
        argString = '-i germany.osm -p input.poly'
        self.creator = MapCreator(shlex.split(argString))
        cmdArgs = self.creator.getArgs()
        # file does not exist, must throw exception
        with self.assertRaises(IOError):
            self.creator.isPolyFileOk(cmdArgs.inputfile)
        # the following infile must be accepted 
        polyfile = self.__dataDir + 'germany.poly'
        self.assertTrue(self.creator.isPolyFileOk(polyfile), "%s is a not valid inputfile" % polyfile)
        # the following infile must not be accepted
        polyfile = self.__dataDir + 'germany.osm'
        self.assertFalse(self.creator.isPolyFileOk(polyfile), "%s is a valid inputfile" % polyfile)    


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))
