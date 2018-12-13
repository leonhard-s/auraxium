from auraxium import *

# Generate a request
my_request = census.get('character',
                        terms={'field': 'name.first_lower',
                               'value': 'higby'},
                        show=['name.first', 'times.creation_date'])

# Retrieve the response
print(my_request.call()['character_list'][0]['times']['creation_date'])
