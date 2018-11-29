# QUERY GENERATOR
# ---------------
# This is a tool used to generate Census API queries and save the reply as a
# JSON document.

import os
from contextlib import redirect_stdout
from datetime import datetime
from json import dump

import auraxium.census as c

# Generate a new request
my_request = c.Request('outfit_member',
                       terms=[['outfit_id', '37557096301203338']],
                       limit=1000,
                       hide=['outfit_id',
                             'member_since_date',
                             'rank',
                             'member_since',
                             'rank_ordinal'])

my_request.join('characters_online_status',
                on='character_id',
                to='character_id',
                nickname='online_status',
                hide=['character_id'])

# Retrieve the server's response
json_data = my_request.retrieve()

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
