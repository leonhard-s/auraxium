# GET COLLECTION FIELDS
# ---------------------
# This script retrieves the fields available in a collection and infers which
# are optional and which ones are not.

import os
from contextlib import redirect_stdout
from datetime import datetime
from json import dump

import auraxium.census as c

# SETTINGS
COLLECTION = 'weapon_datasheet'
EXAMPLE_VALUES = 10
# END OF SETTINGS


print('Retrieving fields for collection "{}":'.format(COLLECTION))
entries = c.census_request(
    'https://census.daybreakgames.com/count/ps2/{}'.format(COLLECTION))['count']

print('Collection has {} entries.'.format(entries))
# The census API will never return more than 100000 items
if entries > 100000:
    print('Capping at 100000.')

object_list = c.census_request('https://census.daybreakgames.com/get/ps2/{}?c:limit={}'.format(
    COLLECTION, entries))['{}_list'.format(COLLECTION)]

# For every entry in the collection
object_dict = {COLLECTION: {}}
for object in object_list:
    for field in object:
        # If the field already exists
        if field in object_dict[COLLECTION].keys():
            # Increment its count
            object_dict[COLLECTION][field]['usage_count'] += 1
            if len(object_dict[COLLECTION][field]['example_values']) < EXAMPLE_VALUES:
                object_dict[COLLECTION][field]['example_values'].append(
                    object[field])
        else:
            object_dict[COLLECTION][field] = {'usage_count': 1}
            object_dict[COLLECTION][field]['example_values'] = [object[field]]

# Find optional and required fields
for field in object_dict[COLLECTION].keys():
    # If the field has not been used in every single object
    if object_dict[COLLECTION][field]['usage_count'] < len(object_list):
        object_dict[COLLECTION][field]['is_optional'] = True
    else:
        object_dict[COLLECTION][field]['is_optional'] = False

# Generate a unique filename for the response file:
filename = 'data/query-test_{}.json'.format(
    datetime.now().strftime('%Y%m%d_%H-%M-%S'))
# Write the returned JSON data into a dump file
with open(filename, 'w') as dump_file:
    dump(object_dict, dump_file)
print('JSON file generated.\n')

# This hides the print statement returned when opening the file
with redirect_stdout(open(os.devnull, "w")):
    # Open the dump file
    os.system('start ' + filename)
