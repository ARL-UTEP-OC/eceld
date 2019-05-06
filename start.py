#!/usr/bin/env python
import logging
import time
from engine.engine import Engine


def execute_tshark_test():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: Removing all previous data")
    engine.delete_all()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining tshark collector")
    c = engine.get_collector("tshark")
    logging.debug("Engine_invoker: starting collector")
    engine.start_collector(c)

def execute_pykeylogger_test():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: Removing all previous data")
    engine.delete_all()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining pykeylogger collector")
    c = engine.get_collector("pykeylogger")
    logging.debug("Engine_invoker: starting collector")
    engine.start_collector(c)

def execute_nmap_test():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: Removing all previous data")
    engine.delete_all()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining nmap collector")
    c = engine.get_collector("nmap")
    logging.debug("Engine_invoker: starting collector")
    engine.start_collector(c)

def execute_manualscreenshot_test():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: Removing all previous data")
    engine.delete_all()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining manualscreenshot collector")
    c = engine.get_collector("manualscreenshot")
    logging.debug("Engine_invoker: starting collector")
    engine.start_collector(c)

def execute_snoopy_test():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: Removing all previous data")
    engine.delete_all()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining snoopy collector")
    c = engine.get_collector("snoopy")
    logging.debug("Engine_invoker: starting collector")
    engine.start_collector(c)

if __name__ == "__main__":
    execute_tshark_test()
    execute_pykeylogger_test()
    execute_nmap_test()
    #execute_manualscreenshot_test()
    execute_snoopy_test()
