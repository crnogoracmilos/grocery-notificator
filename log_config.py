import logging

def setup_logging(level = logging.INFO):
    logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        level=logging.DEBUG)

