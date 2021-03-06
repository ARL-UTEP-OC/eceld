import os
import subprocess

from engine.parser import Parser
from engine.engine import Engine

class auditdParser(Parser):
    type = "parsers.auditd"

    def __init__(self, collector):
        super(auditdParser, self).__init__(collector)
        if os.name == 'nt':
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "auditd_parser.bat")
        else:
            self.script_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "auditd_parser.sh")

#    def do_file(self, file_path):
#        if os.name == 'nt':
#            subprocess.Popen(
#                [self.script_file, file_path, self.parsed_folder], cwd=os.path.dirname(os.path.realpath(__file__)),
#                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
#        else:
#            print "!!!",file_path,"!!!"
#            subprocess.call([self.script_file, file_path, self.parsed_folder])
    def parse(self):
        if os.name == 'nt':
            subprocess.Popen(
                [self.script_file, self.file_or_dir, self.parsed_folder],
                cwd=os.path.dirname(os.path.realpath(__file__)),
                stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        else:
            e = Engine()
            e.incNumParsersRunning()
            s = subprocess.check_call([self.script_file, self.file_or_dir, self.parsed_folder], shell=False)
            e.decNumParsersRunning()
