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
        pass
    
    def __parseCmd(self):
        parser = ArgumentParser(description='Create a Garmin map from OpenStreetMap data')

        mandatory = parser.add_argument_group('mandatory arguments')

        helpMsg = 'one or more JTest XML files'
        parser.add_argument('-f', '--files', action='store', type=str, dest='files',
                            required=False, nargs='+', metavar='FILE', help=helpMsg)

        helpMsg = 'one or more directories including JTest XML files'
        parser.add_argument('-d', '--dirs', action='store', type=str, dest='dirs',
                            required=False, nargs='+', metavar='DIR', help=helpMsg)

        helpMsg = 'scan directories recursive'
        parser.add_argument('-r', '--recursive', action='store_true', dest='recursive',
                            required=False, default=False, help=helpMsg)

        helpMsg = 'CC&S source/SCT base directory. If this parameter is set, --dirs, --files will be ignored'
        parser.add_argument('-b', '--base', action='store', type=str, dest='basedir',
                            required=False, help=helpMsg)

        helpMsg = 'output directory, where result JTest XML files will be stored'
        mandatory.add_argument('-o', '--output', action='store', type=str, dest='outputdir',
                               metavar='OUTPUT', required=True, help=helpMsg) 