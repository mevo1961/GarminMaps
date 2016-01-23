'''
Created on 23.01.2016

@author: mevo
'''
import os
import unittest

from OsmosisCommand import OsmosisCommand


class Test_OsmosisCommand(unittest.TestCase):


    def setUp(self):
        self.__toolsDir = os.path.abspath("../../tools")
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
        self.__osmosisCmd = OsmosisCommand()


    def tearDown(self):
        pass


    def testCutMapWithPolygon_Default(self):
        cmdstr = self.__osmosisCmd.cutMapWithPolygon()
        expectedStr = self.__osmosisTool + ' --read-xml file="germany.osm" --bounding-polygon file="germany.poly" --write-xml file="temp.osm"'
        print cmdstr 
        print expectedStr
        self.assertEqual(expectedStr, cmdstr,  'cmdstring was not composed properly')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCutMapWithPolygon']
    unittest.main()