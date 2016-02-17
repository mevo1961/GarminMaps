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
import glob

sys.path.append('../../src/python')

from MapCreator import MapCreator


class Test_MapCreator_Longrunning(unittest.TestCase):


    def setUp(self):
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
        self.__dataDir = os.path.abspath("../../data") + "/"
        logging.basicConfig(level=logging.DEBUG)


    def tearDown(self):
        pass 

    @unittest.skip("this test is currently disabled")    
    def testCutMapDataWithPolygon(self):
        argString = '-i ' + self.__dataDir + 'baden-wuerttemberg-latest.osm.bz2 -p ' + self.__dataDir + 'tuebingen-regbez.poly'
        outfile = self.__dataDir + "temp.osm"
        self.creator = MapCreator(shlex.split(argString), test=False)
        self.creator.cutMapDataWithPolygon()
        self.creator.checkFileExists(outfile)
        os.remove(outfile)
    
    @unittest.skip("this test is currently disabled")  
    def testCutMapDataWithBoundingBox(self):
        argString = '-i ' + self.__dataDir + 'baden-wuerttemberg-latest.osm.bz2 -t 48.5 -l 9.8 -b 48.4 -r 10.0'
        outfile = self.__dataDir + "temp.osm"
        self.creator = MapCreator(shlex.split(argString), test=False)
        self.creator.cutMapDataWithBoundingBox()
        self.creator.checkFileExists(outfile)
        os.remove(outfile)
        
    def testSplitOsmFileIntoTiles(self):
        # delete the files to be created first if they already exist
        mapid = "6400"
        [ os.remove(filename) for filename in glob.glob(self.__dataDir + "areas.*") ]
        [ os.remove(filename) for filename in glob.glob(self.__dataDir + mapid + "*") ]
        argString = '-i ' + self.__dataDir + 'bremen-latest.osm --mi ' +  mapid
        self.creator = MapCreator(shlex.split(argString), test=False)
        testfile = self.__dataDir + "bremen-latest.osm.pbf"
        self.creator.splitOsmFileIntoTiles(testfile, self.__dataDir)
        self.creator.checkFileExists(self.__dataDir + mapid + "0001.osm.pbf")
        self.creator.checkFileExists(self.__dataDir + "areas.list")
        self.creator.checkFileExists(self.__dataDir + "areas.poly")
        
if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))
