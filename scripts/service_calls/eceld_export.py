#!/usr/bin/env python
import Pyro4
import time
import logging
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.error("usage: eceld_export.py <path>")
        exit()
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Instantiating eceld_export")
    logging.debug("ecel_manager(): getting a handle to the ecel.service")
    ecel_manager = Pyro4.Proxy("PYRONAME:ecel.service")    # use name server object lookup uri shortcut
    logging.debug("ecel_manager(): requesting to start collectors")
    ecel_manager.export_data(sys.argv[1])
    logging.info("Completed eceld_export")
