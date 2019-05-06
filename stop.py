#!/usr/bin/env python
import logging
import time
from engine.engine import Engine


def execute_tshark_stop():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Stopping Program')
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining tshark collector")
    c = engine.get_collector("tshark")
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)

def execute_pykeylogger_stop():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Stopping Program')
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining pykeylogger collector")
    c = engine.get_collector("pykeylogger")
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)

def execute_nmap_stop():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Stopping Program')
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining nmap collector")
    c = engine.get_collector("nmap")
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)

def execute_manualscreenshot_stop():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Stopping Program')
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining manualscreenshot collector")
    c = engine.get_collector("manualscreenshot")
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)

def execute_snoopy_stop():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Stopping Program')
    logging.debug("Engine_invoker: getting engine instance")
    engine = Engine()
    logging.debug("Engine_invoker: invoking print_collector_names")
    engine.print_collector_names()
    logging.debug("Engine_invoker: obtaining snoopy collector")
    c = engine.get_collector("snoopy")
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)
    
def parse_and_export():
	engine = Engine()
	c = engine.get_all_collectors()
	logging.debug("Engine_invoker: parsing data")
	engine.parse_all_collectors_data()
	logging.debug("Engine_invoker: exporting data")
	engine.export('/root/Desktop/')
	logging.debug("Engine_invoker: Complete. Exiting")

if __name__ == "__main__":
    execute_tshark_stop()
    execute_pykeylogger_stop()
    execute_nmap_stop()
    #execute_manualscreenshot_stop()
    execute_snoopy_stop()
    parse_and_export()
