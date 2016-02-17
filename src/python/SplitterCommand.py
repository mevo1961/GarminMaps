'''
Created on 31.01.2016

@author: mevo
'''

import os

class SplitterCommand(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__dataDir = os.path.abspath("../../data") + "/"
        self.__splitterTool = os.path.join(self.__toolsDir, "splitter/splitter.jar")
    
    def splitAreaIntoTiles(self, infile, outdir, mapid):
        cmd = "java -Xmx2000M -jar " + self.__splitterTool + \
              " --mapid=" + mapid + "0001 --max-nodes=800000 --max-areas=20 --output-dir=" + outdir + " " + infile
        return cmd