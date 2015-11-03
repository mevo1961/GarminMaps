'''
Created on 02.11.2015

@author: mevo
'''
import unittest
import datetime
import sys

sys.path.append('../../src/python')

from RunShellCommand import RunShellCommand


class Test(unittest.TestCase):


    def setUp(self):
        self.executor = RunShellCommand()


    def tearDown(self):
        pass
    
    
    def testExecShellCmd(self):
        cmdstring = "ls -l"
        res = self.executor.execShellCmd(cmdstring)
        self.assertEqual(0, res)
        

    def testExecShellCmdWithOutput(self):
        cmdstring = "date +%Y-%m-%d"
        (retcode, output) = self.executor.execShellCmdWithOutput(cmdstring)
        datestring = datetime.date.today().strftime("%Y-%m-%d")
        self.assertEqual(0, retcode, 'executed command failed: %s!' % (cmdstring))
        self.assertEqual(datestring, output.strip(),
             'output of command was wrong: expected "%s", but was "%s"' % (datestring, output.strip()))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExecShellCmd']
    unittest.main()