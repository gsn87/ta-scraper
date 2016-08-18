__author__ = 'gsn'

import json
from pprint import pprint

with open('./output/paris_restaurant.json') as data_file:
	data = json.load(data_file)

# for restaurant in data:
email = []
for i in range(len(data)):
	restaurant_email = data[i]["address"]["email"]
	if restaurant_email != 'none':
		email.append(restaurant_email)
		pprint(restaurant_email)

pprint(len(email))
