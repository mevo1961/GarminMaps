'''
Created on 23.01.2016

@author: mevo
'''
import os
import sys
import unittest
import logging
import time
import xmlrunner

sys.path.append('../../src/python')

from OsmosisCommand import OsmosisCommand


class Test_OsmosisCommand(unittest.TestCase):


    def setUp(self):
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
        self.__osmosisCmd = OsmosisCommand()
        logging.basicConfig(level=logging.DEBUG)


    def tearDown(self):
        pass


    def testCutMapWithPolygon_Default(self):
        cmdstr = self.__osmosisCmd.cutMapWithPolygon()
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-polygon file="germany.poly" --write-xml file="temp.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'cmdstring was not composed properly')
    
    def testCutMapWithPolygon_Parameters(self):
        cmdstr = self.__osmosisCmd.cutMapWithPolygon(infile="input.osm", outfile="output.osm", poly="borders.poly")
        expectedStr = self.__osmosisTool + ' --read-xml file="input.osm" --bounding-polygon file="borders.poly" --write-xml file="output.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'cmdstring was not composed properly')
        
    def testCutMapWithBoundingBox_Default(self):
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox()
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-box top=55.2 left=5.7 bottom=47.2 right=15.1 --write-xml file="temp.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'cmdstring was not composed properly')
        
        
    def testCutMapWithBoundingBox_Parameters(self):
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox(top=49.5138, left=10.9351, bottom=49.3866, right=11.201)
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-box top=49.5138 left=10.9351 bottom=49.3866 right=11.201 --write-xml file="temp.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'cmdstring was not composed properly')

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))