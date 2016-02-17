'''
Created on 25.10.2015

@author: mevo
'''

from argparse import ArgumentParser
import shlex
import sys
import os
import logging

from ShellCommand import ShellCommand
from OsmosisCommand import OsmosisCommand
from SplitterCommand import SplitterCommand

class MapCreator(object):
    '''
    classdocs
    '''


    def __init__(self, options, test = False):
        '''
        Constructor
        '''
        self.__cmdArgs = self.parseCmdLine(options)
        self.__toolsDir = os.path.abspath("../../tools") + "/"
        self.__dataDir = os.path.abspath("../../data") + "/"
        self.__osmosisCmd = OsmosisCommand()
        self.__executor = ShellCommand(test)
        self.__splitterCmd = SplitterCommand()
        self.__extension = self.mapFileExtension(self.__cmdArgs.inputfile)
        logging.basicConfig(level=logging.INFO)
        logging.debug('MapCreator created with testmode = %s' % test)
    
    def parseCmdLine(self, options):
        parser = ArgumentParser(description='Create a Garmin map from OpenStreetMap data')

        mandatory = parser.add_argument_group('mandatory arguments')

        # coordinate options
        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-b', '--bottom', action='store', type=float, dest='bottom',
                            required=False, default=47.2, help=helpMsg)
        
        helpMsg = 'top coordinate of the area to cut from input data'
        parser.add_argument('-t', '--top', action='store', type=float, dest='top',
                            required=False, default=55.2, help=helpMsg)
        
        helpMsg = 'western coordinate of the area to cut from input data'
        parser.add_argument('-l', '--left', action='store', type=float, dest='left',
                            required=False, default=5.7, help=helpMsg)
        
        helpMsg = 'eastern coordinate of the area to cut from input data'
        parser.add_argument('-r', '--right', action='store', type=float, dest='right',
                            required=False, default=15.1, help=helpMsg)
        
        helpMsg = 'path of polygon file'
        parser.add_argument('-p', '--poly', action='store', type=str, dest='poly',
                            required=False, help=helpMsg)
        
        # contourline options
        helpMsg = 'distance between minor contour lines'
        parser.add_argument('--ci', '--contour-step-min', action='store', type=int, dest='cstepmin',
                            required=False, default=10, help=helpMsg)
        
        helpMsg = 'distance between medium contourlines'
        parser.add_argument('--ce', '--contour-step-med', action='store', type=int, dest='cstepmed',
                            required=False, default=50, help=helpMsg)
        
        helpMsg = 'distance between major contourlines'
        parser.add_argument('--ca', '--contour-step-max', action='store', type=int, dest='cstepmax',
                            required=False, default=100, help=helpMsg)
        
        # mapid and mapname options
        helpMsg = 'map id (a unique 4 digit integer)'
        parser.add_argument('--mi', '--map-id', action='store', type=int, dest='mapid',
                            required=False, default=6400, help=helpMsg)
        
        helpMsg = 'mapname (a string giving a name to the map)'
        parser.add_argument('--mn', '--map-name', action='store', type=str, dest='mapname',
                            required=False, default='GER', help=helpMsg)
        
        # family ids for main map and contour maps
        helpMsg = 'family id (a unique 4 digit integer)'
        parser.add_argument('--fi', '--family-id', action='store', type=int, dest='famid',
                            required=False, default=1441, help=helpMsg)
        
        helpMsg = 'minor contourmap family id (a unique 4 digit integer)'
        parser.add_argument('--cid', '--contour-min-family-id', action='store', type=int, dest='cminid',
                            required=False, default=2441, help=helpMsg)
        
        helpMsg = 'major contourmap family id (a unique 4 digit integer)'
        parser.add_argument('--cad', '--contour-max-family-id', action='store', type=int, dest='cmaxid',
                            required=False, default=2443, help=helpMsg)
        
        # nocontours flag
        helpMsg = 'scan directories recursive'
        parser.add_argument('--nc', '--no-contours', action='store_true', dest='nocontours',
                            required=False, default=False, help=helpMsg)
        
        # inputfile option
        helpMsg = 'input file containing OpenStreetMap data'
        mandatory.add_argument('-i', '--input', action='store', type=str, dest='inputfile',
                               required=True, help=helpMsg)
        
        args = parser.parse_args(options)
        return args
    
    def getArgs(self):
        return self.__cmdArgs
    
    def mapFileExtension(self, infile):
        (dummy, extension) = os.path.splitext(infile)
        if (not self.isKnownDataFileExtension(extension)):
            raise ValueError('unknown input file extension', extension)
        mapExtension = { '.osm' : '.osm', '.bz2' : '.osm', '.pbf' : '.osm.pbf'}
        ending = mapExtension[extension]
        return ending
    
    def cutMapDataWithPolygon(self):
        self.isDataFileOk(self.getArgs().inputfile)
        self.isPolyFileOk(self.getArgs().poly)
        cmdstr = self.__osmosisCmd.cutMapWithPolygon(infile=self.getArgs().inputfile, 
                                                     outfile=self.__dataDir + "temp" + self.__extension,
                                                     poly=self.getArgs().poly)
        logging.debug('cutMapDataWithPolygon: cmdstr = %s' % cmdstr)
        res = self.__executor.execShellCmd(cmdstr)
        return res
    
    def cutMapDataWithBoundingBox(self):
        self.isDataFileOk(self.getArgs().inputfile)
        cmdstr = self.__osmosisCmd.cutMapWithBoundingBox(infile  = self.getArgs().inputfile, 
                                                         outfile = self.__dataDir + "temp" + self.__extension,
                                                         top     = self.getArgs().top,
                                                         left    = self.getArgs().left,
                                                         bottom  = self.getArgs().bottom,
                                                         right   = self.getArgs().right)
        logging.debug('cutMapDataWithBoundingBox: cmdstr = %s' % cmdstr)
        res = self.__executor.execShellCmd(cmdstr)
        return res
    
    def isKnownDataFileExtension(self, file_extension):
        return file_extension in ('.bz2', '.osm', '.pbf')
      
    def isKnownPolyFileExtension(self, inputfile):
        dummy, file_extension = os.path.splitext(inputfile)
        return file_extension in ('.poly', '.txt')
    
    def checkFileExists(self, infile):
        # the following statement will throw an exception if the input file can't be read
        with open(infile, 'r'):
            pass
        return True
    
    def isDataFileOk(self, datafile):
        self.checkFileExists(datafile)
        dummy, file_extension = os.path.splitext(datafile)
        return self.isKnownDataFileExtension(file_extension)
    
    def isPolyFileOk(self, polyfile):
        self.checkFileExists(polyfile)
        return self.isKnownPolyFileExtension(polyfile)
    
    def splitOsmFileIntoTiles(self, inputfile, outputdir):
        self.isDataFileOk(self.getArgs().inputfile)
        cmdstr = self.__splitterCmd.splitAreaIntoTiles(inputfile, outputdir, str(self.getArgs().mapid))
        logging.debug('splitOsmFileIntoTiles: cmdstr = %s' % cmdstr)
        res = self.__executor.execShellCmd(cmdstr)
        return res
        
          
if __name__ == "__main__":
    args = MapCreator(sys.argv[1:]).getArgs()
    print ("inputfile = %s") % (args.inputfile)
    print (args)
