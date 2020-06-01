from engine.collector import AutomaticCollector
import os

class pykeylogger(AutomaticCollector):
    def build_commands(self):
        self.commands.append("python3 keylogger.py")