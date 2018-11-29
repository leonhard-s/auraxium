import auraxium.census as c

# Generate a request
my_request = c.Request('character',
                       terms=[['name.first_lower', 'higby']],
                       show=['name.first', 'times.creation_date'])

# Retrieve the response
print(my_request)
