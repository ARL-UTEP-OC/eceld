#!/usr/bin/env python
import Pyro4
import time
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Instantiating eceld_parse")
    logging.debug("ecel_manager(): getting a handle to the ecel.service")
    ecel_manager = Pyro4.Proxy("PYRONAME:ecel.service")    # use name server object lookup uri shortcut
    logging.debug("ecel_manager(): requesting to parse data")
    ecel_manager.parse_data_all()
    logging.info("Completed eceld_parse")
