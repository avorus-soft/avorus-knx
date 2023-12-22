import logging

logger = logging.getLogger()
FORMAT = '%(asctime)s.%(msecs)03d:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT,
                    datefmt='%y-%m-%d %H:%M:%S')
