from engine.collector import AutomaticCollector
import os
import shlex
import subprocess

class pykeylogger(AutomaticCollector):
    def pykeylogger_config_cmd(self, command):
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
        self.commands.append("python3 keylogger.py")

    def run(self):
        # additional logic to allow access to X11
        self.pykeylogger_config_cmd("xhost +SI:localuser:root")
        #now start the collector
        super(pykeylogger, self).run()

    def terminate(self):
        #additional logic to disable access to X11
        self.pykeylogger_config_cmd("xhost -SI:localuser:root")
        #Now stop the collector
        super(pykeylogger, self).terminate()
