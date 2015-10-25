'''
Created on 25.10.2015

@author: mevo
'''

from argparse import ArgumentParser

class MapCreator(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.__cmdArgs = self.__parseCmd()
    
    def __parseCmd(self):
        parser = ArgumentParser(description='Create a Garmin map from OpenStreetMap data')

        mandatory = parser.add_argument_group('mandatory arguments')

        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-b', '--bottom', action='store', type=str, dest='bottom',
                            required=False, help=helpMsg)
        
        helpMsg = 'top coordinate of the area to cut from input data'
        parser.add_argument('-t', '--top', action='store', type=str, dest='top',
                            required=False, help=helpMsg)
        
        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-l', '--left', action='store', type=str, dest='left',
                            required=False, help=helpMsg)
        
        helpMsg = 'bottom coordinate of the area to cut from input data'
        parser.add_argument('-r', '--right', action='store', type=str, dest='right',
                            required=False, help=helpMsg)



        helpMsg = 'input file containing OpenStreetMap data'
        mandatory.add_argument('-i', '--input', action='store', type=str, dest='inputdir',
                               metavar='INPUT', required=True, help=helpMsg) 