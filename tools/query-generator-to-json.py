# QUERY GENERATOR
# ---------------
# This is a tool used to generate Census API queries and save the reply as a
# JSON document.

import os
from contextlib import redirect_stdout
from datetime import datetime
from json import dump

from auraxium import *

# Generate a new request
my_request = census.get('outfit_member',
                        terms={'field': 'outfit_id',
                               'value': '37557096301203338'},
                        limit=1000,
                        show='character_id')

my_request.join('characters_online_status',
                match='character_id',
                hide='character_id')

# Retrieve the server's response
json_data = my_request.call()

# Generate a unique filename for the output file:
filename = 'data/query-test_{}.json'.format(
    datetime.now().strftime('%Y%m%d_%H-%M-%S'))

# Write the returned JSON data into a dump file
with open(filename, 'w') as dump_file:
    dump(json_data, dump_file)

# The following hides the hidden print statement
with redirect_stdout(open(os.devnull, "w")):
    # Open the dump file
    os.system('start ' + filename)
