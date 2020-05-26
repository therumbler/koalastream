"""kick it all off"""

import logging
import sys

from koalastream.web import make_api, make_web


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
internal_api = make_api()
external_app = make_web()
