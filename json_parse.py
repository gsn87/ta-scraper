__author__ = 'gsn'

import json
import csv
from pprint import pprint

with open('./output/all.json') as data_file:
	data = json.load(data_file)

# for restaurant in data:
email = []

with open('./output/LyonMarsToulBord.csv', 'wb') as csvfile:
	print('name \t email \t phone \t street \t cp \t city')
	writer = csv.writer(csvfile, delimiter='\t')
	for i in range(len(data)):
		# print data[i]["address"]
		name = data[i]["name"]
		# phone = data[i]["address"]["phone"]
		mail = data[i]["address"]["email"].encode('utf-8')
		street = data[i]["address"]["street"]
		# cp = data[i]["address"]["postal_code"]
		try:
			city = data[i]["address"]["locality"]
		except:
			pass
		if mail != 'none':
			if city == 'Lyon' or city == 'Marseille' or city == 'Toulouse' or city == 'Bordeaux' :
				email.append(mail)
				# print('%s \t %s' % (name, mail))
				print name, mail
				writer.writerow([name, mail])

pprint(str(len(email)) + '/' + str(len(data)))
