"""Utility methods to simplify the creation of unit tests."""

import os

DATA = os.path.abspath('tests/data')
SERVICE_ID = os.environ.get('SERVICE_ID', 's:example')
