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
    logging.debug("Engine_invoker: waiting 5 seconds")
    time.sleep(5)
    logging.debug("Engine_invoker: stopping collector")
    engine.stop_collector(c)
    logging.debug("Engine_invoker: parsing data")
    engine.parser(c)
    logging.debug("Engine_invoker: Complete. Exiting")

if __name__ == "__main__":
    execute_tshark_test()