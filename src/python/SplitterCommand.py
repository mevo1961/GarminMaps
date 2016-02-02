'''
Created on 31.01.2016

@author: mevo
'''

import os
import logging

class SplitterCommand(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__splitterTool = os.path.join(self.__toolsDir, "splitter/lib/splitter.jar")
        self.__dataDir = os.path.abspath("../../data") + "/"
    
    def splitAreaIntoTiles(self, infile):
        cmd = "java -Xmx2000M -jar " + self.__splitterTool + \
              " --mapid=${MAPID}0001 --max-nodes=800000 --max-areas=20 " + infile
        return cmd