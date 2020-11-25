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
        self.clean()
        self.create_confd()
        # build command to listen on eth0
        cmd = "suricata"
        cmd += " -c " + self.config_filename
        cmd += " -i eth0"
        cmd += " -l " + self.output_dir
        cmd += " -s " + self.suricata_rules_filename
        cmd += " -k none"

        self.commands.append(cmd)

    def create_confd(self):

        try:
            # path to rules
            self.suricata_rules_filename = self.config.get_collector_custom_data()["rule path"]

            # path to yaml file
            self.config_filename = self.config.get_collector_custom_data()["config path"]

        except:
            self.logger.error("Could not create confd file")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
