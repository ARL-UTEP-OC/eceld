#!/usr/bin/env python
import Pyro4
import time
import logging
from subprocess import Popen

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("Instantiating ecel_manager()")
    
    logging.debug("ecel_manager(): getting a handle to the ecel.service")
    ecel_manager = Pyro4.Proxy("PYRONAME:ecel.service")    # use name server object lookup uri shortcut
    logging.debug("ecel_manager(): requesting to remove all data")
    ecel_manager.remove_data()
    logging.debug("ecel_manager(): requesting to start collectors")
    ecel_manager.start_collectors()
    logging.debug("ecel_manager(): sleeping for 5 seconds")
    time.sleep(5)
    logging.debug("ecel_manager(): requesting to stop collectors")
    ecel_manager.stop_collectors()
    logging.debug("ecel_manager(): requesting to export data to /root/Desktop/")
    ecel_manager.export_data(path="/root/Desktop/")
    logging.info("Completed ecel_manager()")
