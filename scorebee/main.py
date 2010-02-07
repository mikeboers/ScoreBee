
import logging
import sys

from .application import Application


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Application(sys.argv).run()