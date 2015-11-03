'''
Created on 25.10.2015

@author: mevo
'''

from argparse import ArgumentParser
import sys
import os

from RunShellCommand import RunShellCommand

class MapCreator(object):
    '''
    classdocs
    '''


    def __init__(self, options):
        '''
        Constructor
        '''
        self.__cmdArgs  = self.parseCmdLine(options)
        self.__toolsDir = os.path.abspath("../../tools")
        self.__dataDir  = os.path.abspath("../../data")
        self.__executor = RunShellCommand()
    
    def parseCmdLine(self, options):
        parser = ArgumentParser(description='Create a Garmin map from OpenStreetMap data')
        # parser = ArgumentParser()

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
    
    
    def cutOutMapData(self):
        self.__osmosisdir = os.path.join(self.__toolsDir, "osmosis/bin/osmosis")
        cmdstr = self.__osmosisdir + "--help"
        print cmdstr
        res = self.__executor.execShellCmd(cmdstr)
        return res
        
    
if __name__ == "__main__":
    args = MapCreator(sys.argv[1:]).getArgs()
    print ("inputfile = %s") % (args.inputfile)