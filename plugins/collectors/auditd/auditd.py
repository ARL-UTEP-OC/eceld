import os
import definitions
from engine.collector import AutomaticCollector
import shlex
import subprocess

class auditd(AutomaticCollector):
    def auditd_config_cmd(self, command):
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
        # get additional options from config.json
        self.auditdConfigPath = self.config.get_collector_custom_data()["config path"]
        self.auditdRulePath = self.config.get_collector_custom_data()["rule path"]
        # build commands
        out_file_name = definitions.TIMESTAMP_PLACEHOLDER + "_" + "auditd"
        out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")
        #TODO: need to recreate the config file with the name of log file here
        #command to replace logfile name
        #command to copy files to respective locations
        #Append command to start auditd
        cmd = "auditctl -s enable"
        self.commands.append(cmd)
        
    #TODO: I probably don't need this since I hold the proc id and then kill it...
    def terminate(self):
        #additional logic to disable the auditd library
        self.auditd_config_cmd("auditctl -s disable")
        #Now stop the collector
        super(auditd, self).terminate()

