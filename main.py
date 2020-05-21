"""kick it all off"""

import logging
import sys

from koalastream.web import make_api


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
api = make_api()
