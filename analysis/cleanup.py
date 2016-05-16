#!/usr/bin/python

import csv
import json

# The number of questions in the survey. Any entry with a different number will be dropped.
# This needs to be adjusted if used for a different study
NUMQUESTIONS = 60

hits = json.load(open('pie-variations-data.json', 'rb'))

workers = []
data = []
for hit in hits:
#	if 'workerId' not in hit:
#		print hit
	worker = {'workerID': hit['workerId']}

	hitObject = {}
	for key in hit:
		dash = key.rfind('-')
		hitKey = key[:dash]
		index = key[dash+1:]

		if index.isdigit():

			if index not in hitObject:
				hitObject[index] = { 'workerID': hit['workerId'] }

			hitObject[index][hitKey] = hit[key]

		else:
			worker[key] = hit[key]

	if len(hitObject.keys()) == NUMQUESTIONS:
		data.append(hitObject)
		workers.append(worker)
	elif len(hitObject.keys()) == NUMQUESTIONS: # Finding too many means NUMQUESTIONS is probably wrong
		print 'Too many records ('+str(len(hitObject.keys()))+') for '+hit['workerId']

# Turn into long list and count flipped values
datalist = []
for hitObject in data:
	numReversed = 0
	workerID = ''
	for key in hitObject:
		workerID = hitObject[key]['workerID']
		if hitObject[key]['ans-trial'].isdigit():
			answer = int(hitObject[key]['ans-trial'])
		else:
			answer = 0
		if abs(100-answer-int(hitObject[key]['correct-ans'])) < abs(answer-int(hitObject[key]['correct-ans'])):
			numReversed += 1

	if numReversed >= NUMQUESTIONS/10:
		print workerID+': '+str(float(numReversed)/NUMQUESTIONS*100)

	for key in hitObject:
		hitObject[key]['totalSequence'] = key
		if 'time_diff_time-trial' in hitObject[key]:
			hitObject[key]['time_diff_time-trial'] = str(float(hitObject[key]['time_diff_time-trial'])/1000)
		datalist.append(hitObject[key])

with open('pie-variations-reshaped-unique.csv', 'wb') as outFile:
	outCSV = csv.DictWriter(outFile, datalist[0].keys())

	outCSV.writeheader()
	outCSV.writerows(datalist)

with open('pie-variations-demographics.csv', 'wb') as outFile:
	outCSV = csv.DictWriter(outFile, workers[0].keys())

	outCSV.writeheader()
	outCSV.writerows(workers)

print str(len(workers))+' workers, '+str(len(datalist))+' records.'
