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
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-polygon file="germany.poly" completeWays=no --write-xml file="temp.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))
    
    def testCutMapWithPolygon_Parameters(self):
        cmdstr = self.__osmosisCmd.cutMapWithPolygon(infile="input.osm", outfile="output.osm", poly="borders.poly")
        expectedStr = self.__osmosisTool + ' --read-xml file="input.osm" --bounding-polygon file="borders.poly" completeWays=no --write-xml file="output.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))
        
    def testCutMapWithPolygon_Parameters_pbf(self):
        cmdstr = self.__osmosisCmd.cutMapWithPolygon(infile="input.osm.pbf", outfile="output.osm.pbf", poly="borders.poly")
        expectedStr = self.__osmosisTool + ' --read-pbf file="input.osm.pbf" --bounding-polygon file="borders.poly" completeWays=no --write-pbf file="output.osm.pbf"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))
        
    def testCutMapWithBoundingBox_Default(self):
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox()
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-box top=55.2 left=5.7 bottom=47.2 right=15.1 completeWays=no --write-xml file="temp.osm"'
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))
        
    def testCutMapWithBoundingBox_Parameters(self):
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox(top=49.5138, left=10.9351, bottom=49.3866, right=11.201)
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-box top=49.5138 left=10.9351 bottom=49.3866 right=11.201 completeWays=no --write-xml file="temp.osm"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))
        
    def testCutMapWithBoundingBox_Parameters_pbf(self):
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox(infile="germany.osm.pbf", top=49.5138, left=10.9351, bottom=49.3866, right=11.201, outfile="temp.osm.pbf")
        expectedStr = self.__osmosisTool + ' --read-pbf file="germany.osm.pbf" --bounding-box top=49.5138 left=10.9351 bottom=49.3866 right=11.201 completeWays=no --write-pbf file="temp.osm.pbf"'
        logging.debug('cmdstr   = %s' % cmdstr)
        logging.debug('expected = %s' % expectedStr)
        self.assertEqual(expectedStr, cmdstr,  'unexpected cmdstr, \nexpected: %s,\nbut was:  %s' % (expectedStr, cmdstr))

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output = 'test-reports', outsuffix = time.strftime("%Y%m%d%H%M%S")))