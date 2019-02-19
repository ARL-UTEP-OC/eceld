import os
import definitions
from engine.collector import AutomaticCollector

class nmap(AutomaticCollector):


    def build_commands(self):
        self.clean()

        option = self.config.get_collector_custom_data()["interfaces"]["additional options"]
        network = self.config.get_collector_custom_data()["interfaces"]["ip range"]
        out_file_name = "nmap_" + definitions.TIMESTAMP_PLACEHOLDER

        self.output_filenames.append(out_file_name)

        out_file_path = os.path.join(self.output_dir, out_file_name + ".xml")
        # build commands
        cmd = self.name + option + " " + network + " -oX " + out_file_path
        if (os.name == "nt"):
            cmd = cmd.replace("\\", "/")  # Needed in windows to ensure output file is placed in correct directory.

        self.commands.append(cmd)