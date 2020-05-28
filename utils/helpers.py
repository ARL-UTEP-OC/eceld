#this file contains common functions to be used through ECEL

import subprocess
import shlex
import logging

#executes system command
#takes shell command to execute as input
def execCommand(cmd):
    runcmd = shlex.split(cmd)
    try:
        process = subprocess.check_call(runcmd)
        
    except subprocess.CalledProcessError as err:
        logging.error("Error attempting to run command : %s\n" % (cmd))
        logging.error("System Error:" + str(err))
        
    except OSError as err:
        logging.error("Error attempting to run command : %s\n" % (cmd))
        logging.error("System Error:" + str(err))