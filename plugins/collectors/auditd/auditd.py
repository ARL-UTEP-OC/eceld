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
        # build commands
        #command to replace logfile name
        self.create_confd()
        #command to copy files to respective locations
        self.copy_rules()
        #Append command to start auditd
        cmd = "service auditd start"
        self.commands.append(cmd)
        
    def create_confd(self):
        try:
            # path to template exists in the collector subfolder
            path_to_templates = os.path.join(self.base_dir,'config')
            env = Environment(loader=FileSystemLoader(path_to_templates))
            
            # log file should be saved to plugin output folder
            out_file_name = str(int(time.time())) + "_" + "auditd"
            out_file_path = os.path.join(self.output_dir, out_file_name + ".txt")

            # substitute the text to name the log file using epoch time
            template = env.get_template('auditd.conf.template')
            output_from_parsed_template = template.render(log_location=out_file_path)
          
            # save the config file to where was indicated in the plugin config
            self.auditdConfigPath = self.config.get_collector_custom_data()["config path"]
            with open(self.auditdConfigPath, "w") as fh:
                fh.write(output_from_parsed_template)
        except:
            self.logger.error("Could not create confd file")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    def copy_rules(self):
        try:
            # path to rule is in the collector subfolder
            path_to_rule = os.path.join(self.base_dir,'config',"audit.rules")
                      
            # save the config file to where was indicated in the plugin config
            self.auditdRulePaths = self.config.get_collector_custom_data()["rule paths"]
            for path in self.auditdRulePaths:
                shutil.copy(path_to_rule, self.auditdRulePatha)
        except:
            self.logger.error("Could not copy rules file")
            exc_type, exce_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exce_value, exc_traceback)

    def terminate(self):
        #additional logic to stop auditd using the service subsystem
        self.auditd_config_cmd("service auditd stop")
        #Now stop the collector
        super(auditd, self).terminate()

