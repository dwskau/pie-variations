#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import math
from scipy.integrate import quad

RADIUS = 155.
OUTER_RADIUS = 175.
ELLIPSE_A = 87.5
ELLIPSE_B = 175.


# Absolute square arc and area for given size and angle,
# starting at vertical for 0 and going counter-clockwise
def squareArcArea(size, angle):
	arc = 0
	area = 0
	eighths = 0
	while angle > math.pi / 4:
		arc += size / 2
		area += size * size / 8
		angle -= math.pi / 4
		eighths += 1

	if eighths % 2 == 0:			# starts at a vertical or horizontal edge
		arc += (size / 2) * math.tan(angle)
		area += size * size * math.tan(angle) / 8
	else:							# starts on a diagonal
		arc += (size / 2) * (1 - math.tan(math.pi/4 - angle))
		area += size * size * (1 - math.tan(math.pi/4 - angle)) / 8

	return [arc, area]

# Calculate 'arc' length and area for a square
def calcSquare(size, angle, rotation):
	angleplusrot = squareArcArea(size, angle+rotation)

	rotonly = squareArcArea(size, rotation)

	return [angleplusrot[0]-rotonly[0], angleplusrot[1]-rotonly[1]]


def ellipseArea(a, b, angle):
	area = 0
	quarters = 0
	while angle > math.pi / 2:
		area += a * b * math.pi / 4
		angle -= math.pi / 2
		quarters += 1

	if quarters % 2 == 0: # starts at a vertical edge
		area += a * b * math.pi / 4 - \
				.5 * a * b * math.atan(a * math.tan(math.pi / 2 - angle) / b)
	else: # starts at horizontal edge
		area += .5 * a * b * math.atan(a * math.tan(angle) / b)

	return area

# Function to integrate from 0 to 2π to get ellipse perimeter
def ellipseArcFunction(t, params):
	a, b = params
	return math.sqrt(a*a * math.sin(t)*math.sin(t) + b*b * math.cos(t)*math.cos(t))

def ellipseArc(a, b, angle):
	length, err = quad(ellipseArcFunction, 0, angle, [a, b])
	return length

# Calculate arc length and area for ellipse
def calcEllipse(a, b, angle, rotation):
	area = ellipseArea(a, b, angle+rotation) - ellipseArea(a, b, rotation)

	arc = ellipseArc(a, b, angle+rotation) - ellipseArc(a, b, rotation)

	return [arc, area]


ellipseTotal = calcEllipse(ELLIPSE_A, ELLIPSE_B, math.pi*2, 0)

inputFieldnames = []
with open('pie-variations-reshaped-unique.csv', 'rb') as inFile:
	reader = csv.DictReader(inFile)

	inputFieldnames = reader.fieldnames

	outRows = []
	for row in reader:

		variation = row['chart-type']
		percentage = float(row['correct-ans'])
		angle = math.pi * 2 * percentage / 100
		rotation = math.radians(float(row['rotation']))

		if variation == 'pie':							# for the pie, the prediction is the exact angle
			row['arcPrediction']  = percentage
			row['areaPrediction'] = percentage
		elif variation == 'outerRadius' or variation == 'exploded': # for larger and exploded pie, it's increased by the outer radius
			row['arcPrediction']  = percentage*OUTER_RADIUS/RADIUS
			row['areaPrediction'] = percentage*(OUTER_RADIUS*OUTER_RADIUS)/(RADIUS*RADIUS)
		elif variation == 'square':
			square = calcSquare(OUTER_RADIUS, angle, rotation)
			row['arcPrediction']  = square[0]/(4*OUTER_RADIUS)*100
			row['areaPrediction'] = square[1]/(OUTER_RADIUS*OUTER_RADIUS)*100
		elif variation == 'ellipse':
			ellipse = calcEllipse(ELLIPSE_A, ELLIPSE_B, angle, rotation)
			row['arcPrediction']  = ellipse[0]/ellipseTotal[0]*100
			row['areaPrediction'] = ellipse[1]/ellipseTotal[1]*100
		else:
			print 'Unknown variation: '+variation

		outRows.append(row)

with open('pie-variations-enriched.csv', 'wb') as outFile:
	inputFieldnames += ['arcPrediction', 'areaPrediction']
	writer = csv.DictWriter(outFile, inputFieldnames)

	writer.writeheader()
	writer.writerows(outRows)

with open('predictions.csv', 'wb') as outFile:
	csvOut = csv.writer(outFile)

	csvOut.writerow(['angle', 'variation', 'arc', 'area'])

	t = 0
	while t < 360:

		radians = math.radians(t)

		csvOut.writerow([t, 'pie', radians/(math.pi*2), radians/(math.pi*2)])

		csvOut.writerow([t, 'outerPie', radians/(math.pi*2)*OUTER_RADIUS/RADIUS, radians/(math.pi*2)*(OUTER_RADIUS*OUTER_RADIUS)/(RADIUS*RADIUS)])

		square = calcSquare(OUTER_RADIUS, radians, 0)
		csvOut.writerow([t, 'square', square[0]/(4*OUTER_RADIUS), square[1]/(OUTER_RADIUS*OUTER_RADIUS)])

		ellipse = calcEllipse(ELLIPSE_A, ELLIPSE_B, radians, 0)
		csvOut.writerow([t, 'ellipse', ellipse[0]/ellipseTotal[0], ellipse[1]/ellipseTotal[1]])

		t += 0.5
