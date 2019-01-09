import logging

import auraxium as arx
from auraxium.util import name_to_id

# Logging
logger = logging.getLogger('auraxium')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('auraxium.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(
    '[%(asctime)s] (%(name)s) - [%(levelname)s] %(message)s'))
ch.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(fh)
logger.addHandler(ch)

# Sandbox
# -----------------------------------------------------------------------------

# Put actual code here
