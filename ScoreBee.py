
import logging
import sys

from scorebee.application import Application

logging.basicConfig(level=logging.INFO)
app = Application(sys.argv)
app.run()