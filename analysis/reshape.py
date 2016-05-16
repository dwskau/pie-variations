#!/usr/bin/python

import csv

r = csv.reader(open('pilot.csv', 'rb'))

data = {}
for row in r:
	dash = row[0].rfind('-')
	key = row[0][:dash]
	index = row[0][dash+1:]

	if index.isdigit():

		if index not in data:
			data[index] = {}

		data[index][key] = row[1]

keys = data.keys()
keys.sort()

allKeys = set()
datalist = []
for k in keys:
	data[k]['totalSequence'] = k
	datalist.append(data[k])
	allKeys = allKeys | set(data[k].keys())

with open('pilot-reshaped.csv', 'wb') as outFile:
	outCSV = csv.DictWriter(outFile, allKeys, delimiter='\t')

	outCSV.writeheader()
	outCSV.writerows(datalist)
