"""kick it all off"""

import logging
import sys

from koalastream.web import make_api, make_web


fmt = "[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] [%(funcName)s] [%(message)s]"
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=fmt)
internal_api = make_api()
external_app = make_web()
