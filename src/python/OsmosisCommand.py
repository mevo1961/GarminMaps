'''
Created on 23.01.2016

@author: mevo
'''

import os

class OsmosisCommand(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__toolsDir = os.path.abspath("../../tools")
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
          
    def cutMapWithPolygon(self, infile="germany.osm", outfile="temp.osm", poly="germany.poly"):
        cmd = self.__osmosisTool                          + \
              ' --read-xml file="'         + infile  + '"' + \
              ' --bounding-polygon file="' + poly    + '"' + \
              ' --write-xml file="'        + outfile + '"'
              
        return cmd 