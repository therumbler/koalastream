"""kick it all off"""

import logging
import sys

from koalastream.web_external import make_web


fmt = "[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] [%(funcName)s] [%(message)s]"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=fmt)
external_app = make_web()
