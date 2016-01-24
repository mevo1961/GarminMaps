'''
Created on 02.11.2015

@author: mevo
'''

import shlex
import subprocess

class ShellCommand(object):
    '''
    classdocs
    '''


    def __init__(self, test=False):
        '''
        Constructor
        '''
        self.__test = test
    
    
    def execShellCmd(self, cmdstring):
        command = shlex.split(cmdstring)
        if self.__test:
            res = cmdstring
        else:
            res = subprocess.call(command)
        return res
    
    def execShellCmdWithOutput(self, cmdstring):
        command = shlex.split(cmdstring)
        if self.__test:
            result = 0
            output = cmdstring
        else:
            tmp = subprocess.Popen(command, stdout=subprocess.PIPE)
            tmp.wait()
            result = tmp.returncode
            output = tmp.stdout.read()
        return (result, output)
