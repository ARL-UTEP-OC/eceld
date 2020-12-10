import os
import definitions
from engine.collector import AutomaticCollector
import shlex
import os
import subprocess
from jinja2 import Environment, FileSystemLoader
import sys, traceback
import time
import shutil

class suricata(AutomaticCollector):
    def suricata_config_cmd(self, command):
        runcmd = shlex.split(command)

        try:
            subprocess.Popen(runcmd,
                             shell=False,
                             cwd=self.base_dir,
                             stdout=self.devnull,
                             stderr=self.devnull)

        except OSError as err:
            self.logger.error("Error attempting to run command in collector: %s | command: %s\n" % (self.name, command))
            self.logger.error("System Error:" + str(err))

    def build_commands(self):
        # build commands
        #self.create_confd()
        #command to copy files to respective locations
        #self.copy_rules()
        #Append command to start suricata
        cmd = "sudo service suricata start"
        self.commands.append(cmd)

    def terminate(self):
        #additional logic to stop suricata using the service subsystem
        self.suricata_config_cmd("sudo service suricata stop")
        #Now stop the collector
        super(suricata, self).terminate()
