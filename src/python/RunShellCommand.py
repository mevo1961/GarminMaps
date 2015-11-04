'''
Created on 02.11.2015

@author: mevo
'''

import shlex
import subprocess

class RunShellCommand(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    
    def execShellCmd(self, cmdstring):
        command = shlex.split(cmdstring)
        res = subprocess.call(command)
        return res
    
    def execShellCmdWithOutput(self, cmdstring):
        command = shlex.split(cmdstring)
        tmp = subprocess.Popen(command, stdout=subprocess.PIPE)
        tmp.wait()
        result = tmp.returncode
        output = tmp.stdout.read()
        return (result, output)
