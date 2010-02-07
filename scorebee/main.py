
import logging
import sys

from .controller import Controller


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Controller(sys.argv).run()