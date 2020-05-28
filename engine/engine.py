import os
import time
import shutil
import logging
import traceback
import subprocess
import definitions

from threading import Event
from threading import Thread
from _version import __version__
from engine.archiver.zip_format import zip
from engine.archiver.tar_format import tar
from engine.archiver.archiver import Archiver
from engine.collector import CollectorConfig, Collector

#TODO: Remove these todos?
#TODO: Handle sigterm correctly, background running thread gets stuck.  Need to use terminate() before quit() or CRTL-C
class Engine(object):
    NUM_PARSER_RUNNING = 0
    def __init__(self):
        self.logger = logging.getLogger('ECEL.engine_logger')
        self.logger.info("ENGINE Logger")
        self.collectors = []
        self.collectors_dir = definitions.PLUGIN_COLLECTORS_DIR

        collector_dirnames = [directory for directory in os.listdir(definitions.PLUGIN_COLLECTORS_DIR) if
                             os.path.isdir(os.path.join(definitions.PLUGIN_COLLECTORS_DIR, directory))]

        for collector_dirname in collector_dirnames:
            if "__pycache__" in collector_dirname:
                continue
            try:
                collector_config = CollectorConfig(collector_dirname)
            except ValueError:
                traceback.print_exc()
            else:
                collector = Collector.factory(collector_config)
                self.collectors.append(collector)

    #TODO: TEST, method from main_gui.py
    def close_all(self):
        for collector in self.collectors:
            if collector.is_enabled:
               self.logger.info("Closing: " + collector.name)
               collector.terminate()


    #TODO: TEST, method from main_gui.py
    def delete_all(self):
        delete_script = "cleanCollectorData.bat" if os.name == "nt" else "cleanCollectorData.sh"
        self.logger.info("Deleting all collector data....")
        remove_cmd = os.path.join(os.path.join(os.getcwd(), "scripts"), delete_script)
        subprocess.call(remove_cmd)  # TODO: Change this to not call external script

    def stop_all_collectors(self):
        for collector in self.collectors:
            if collector.is_enabled():
                self.logger.info("Stopping: " + collector.name)
                collector.terminate()

    #TODO: TEST, method from main_gui.py
    def parse_all_collectors_data(self):
        for collector in self.collectors:
            collector.parser.parse()
            self.logger.info("Parsing " + collector.name)

    #TODO: TEST, method from main_gui.py
    def parser(self, collector):
        self.logger.info("Parsing " + collector.name)
        collector.parser.parse()
    
    def parsersRunning(self):
        if Engine.NUM_PARSER_RUNNING > 0:
            return True
        else:
            return False

    def incNumParsersRunning(self):
        Engine.NUM_PARSER_RUNNING+=1
        
    def decNumParsersRunning(self):
        Engine.NUM_PARSER_RUNNING-=1

    #TODO: TEST, method from main_gui.py
    def start_collector(self, collector):
        self.logger.info("Starting: " + collector.name)
        collector.run()

    #TODO: TEST, mehtod from main_gui.py
    def startall_collectors(self):
        for collector in self.collectors:
            if collector.is_enabled() and isinstance(collector, collector.AutomaticCollector):
                self.logger.info("Starting: "+ collector.name)
                collector.run()

    def stop_collector(self, collector):
        self.logger.info("Stopping: " + collector.name)
        collector.terminate()

    def export(self, export_base_dir, compress_export_format= 'zip', export_raw= True,
    export_compressed= False, export_parsed= True, compress_export =False):

        if export_base_dir == '':
            self.logger.info("Please select a directory to export to.")
            return
        if not os.path.isdir(export_base_dir):
            self.logger.info("Please select a valid directory to export to.")
            return
        if not export_raw and not export_compressed and not export_parsed:
            self.logger.info("Please select at least one data type to export.")
            return

        export_dir = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
            definitions.TIMESTAMP_PLACEHOLDER, "_" + str(int(time.time()))))
        export_raw_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
        export_compressed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
        export_parsed_dir = os.path.join(export_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)
        os.makedirs(export_raw_dir)
        os.makedirs(export_compressed_dir)
        os.makedirs(export_parsed_dir)

        for plugin in next(os.walk(self.collectors_dir))[1]:
            plugin_export_raw_dir = os.path.join(export_raw_dir, plugin)
            plugin_export_compressed_dir = os.path.join(export_compressed_dir, plugin)
            plugin_export_parsed_dir = os.path.join(export_parsed_dir, plugin)
            plugin_collector_dir = os.path.join(self.collectors_dir, plugin)
            plugin_collector_raw_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_OUTPUT_DIRNAME)
            plugin_collector_compressed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_COMPRESSED_DIRNAME)
            plugin_collector_parsed_dir = os.path.join(plugin_collector_dir, definitions.PLUGIN_COLLECTORS_PARSED_DIRNAME)

            if export_raw and os.path.exists(plugin_collector_raw_dir) and os.listdir(plugin_collector_raw_dir):
                shutil.copytree(plugin_collector_raw_dir, plugin_export_raw_dir)
            if export_compressed and os.path.exists(plugin_collector_compressed_dir) and os.listdir(plugin_collector_compressed_dir):
                shutil.copytree(plugin_collector_compressed_dir, plugin_export_compressed_dir)
            if export_parsed and os.path.exists(plugin_collector_parsed_dir) and os.listdir(plugin_collector_parsed_dir):
                shutil.copytree(plugin_collector_parsed_dir, plugin_export_parsed_dir)
            self.logger.info("Copying files " + plugin)

        #Compress export just checks what way to export zip or tar
        if compress_export:
            export_dir_notime = os.path.join(export_base_dir, definitions.PLUGIN_COLLECTORS_EXPORT_DIRNAME.replace(
                definitions.TIMESTAMP_PLACEHOLDER, ""))

            self.logger.info("Compressing data to " + export_dir)

            if compress_export_format == 'zip':
                zip(export_dir, export_dir_notime)
                self.logger.info("Cleaning up " + export_dir)
                self.logger.info("Export complete")
            elif compress_export_format == 'tar':
                tar(export_dir, export_dir_notime)
                self.logger.info("Cleaning up " + export_dir)
                self.logger.info("Export complete")
            else:
                self.logger.info("Incorrect Compression type")
                self.logger.info("Export complete")

    def get_collector(self, name):
        return next(p for p in self.collectors if p.name == name)

    def get_collector_length(self):
        return self.collectors.__len__()

    def has_collectors_running(self):
        for collector in self.collectors:
            if(collector.is_running()):
                return True
        return False

    def print_collector_names(self):
        for i, collector in enumerate(self.collectors):
            self.logger.info("%d) %s" % (i, collector.name))

    def get_all_collectors(self):
        return self.collectors
