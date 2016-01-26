'''
Created on 23.01.2016

@author: mevo

class to deliver an osmosis command as a string
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
        self.__toolsDir = os.path.abspath("../../tools/")
        self.__osmosisTool = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
          
    def cutMapWithPolygon(self, infile="germany.osm", outfile="temp.osm", poly="germany.poly"):
        cmd = self.__osmosisTool                           + \
              ' --read-xml file="'         + infile  + '"' + \
              ' --bounding-polygon file="' + poly    + '"' + \
              ' --write-xml file="'        + outfile + '"'
              
        return cmd
    
    def cutMapWithBoundingBox(self, infile="germany.osm", outfile="temp.osm",
                              top=55.2, left=5.7, bottom=47.2, right=15.1):
        cmd = self.__osmosisTool                                            + \
              ' --read-xml file="'   + infile      + '"'                    + \
              ' --bounding-box top=' + str(top)    + ' left=' + str(left)   + \
              ' bottom='             + str(bottom) + ' right=' + str(right) + \
              ' --write-xml file="'  + outfile     + '"'
        return cmd