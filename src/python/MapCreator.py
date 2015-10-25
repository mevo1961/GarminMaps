'''
Created on 25.10.2015

@author: mevo
'''

from argparse import ArgumentParser
import sys
import shlex

class MapCreator(object):
    '''
    classdocs
    '''


    def __init__(self, options):
        '''
        Constructor
        '''
        # self.__cmdArgs = self.parseCmd(sys.argv[1:])
        self.__cmdArgs = self.parseCmd(options)
    
    def parseCmd(self, options):
        # parser = ArgumentParser(description='Create a Garmin map from OpenStreetMap data')
        parser = ArgumentParser()

        mandatory = parser.add_argument_group('mandatory arguments')

        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-b', '--bottom', action='store', type=float, dest='bottom',
                            required=False, help=helpMsg)
        
        helpMsg = 'top coordinate of the area to cut from input data'
        parser.add_argument('-t', '--top', action='store', type=float, dest='top',
                            required=False, help=helpMsg)
        
        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-l', '--left', action='store', type=float, dest='left',
                            required=False, help=helpMsg)
        
        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-r', '--right', action='store', type=float, dest='right',
                            required=False, help=helpMsg)



        helpMsg = 'input file containing OpenStreetMap data'
        mandatory.add_argument('-i', '--input', action='store', type=str, dest='inputfile',
                               required=True, help=helpMsg)
        
        args = parser.parse_args(options)
        return args
    
    def getArgs(self):
        return self.__cmdArgs
    
if __name__ == "__main__":
    args = MapCreator(sys.argv[1:]).getArgs()
    print ("inputfile = %s") % (args.inputfile)