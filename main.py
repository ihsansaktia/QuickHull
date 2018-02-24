# =============================
# Libraries
# =============================
import os
import random
import numpy as np
from math import atan2
from math import hypot as hyp
import matplotlib.pyplot as plt
# =============================

# If set of points P are used to draw a convex polygon G 
# This function returns a centre point of G
def getCentre(P):
	x = y = 0
	for point in P:
		x += point[0]
		y += point[1]
	lp = len(P)
	centre = [x/lp, y/lp]
	return centre

# For a line L that passes through point A to point B
# This function determines on which side of L is P located 
def whichSide(A, B, P):
	return (P[0]-A[0])*(B[1]-A[1]) - (P[1]-A[1])*(B[0]-A[0])

# For a line L that passes through point A to point B
# This function returns the perpendicular distance from P to L
def distPTL(A, B, P, distAtoB):
	numerator = abs(whichSide(A, B, P))
	return numerator/distAtoB

# This function calculates the distance between point A and point B
def distPTP(A,B):
	return hyp((B[1]-A[1]), (B[0]-A[0]))

# This function initializes recursive calls for finding hulls
def solveQH(P, CH):
	# Sorting set of points by X
	# P.sort()

	# Finding leftmost point, rightmost point
	# Lets say L is a line drawn from leftmost point to rightmost point
	# A random point located at the top of the line L is needed to determine on which side of the line L that a point is located
	leftmost = P[0]
	rightmost = P[-1]
	aTopPoint = [leftmost[0], leftmost[1]+1]
	topSide = whichSide(leftmost, rightmost, aTopPoint)

	# Set of points located in the top side and bottom side of line L respectively
	topP = []
	bottomP = []

	# Dividing points 
	for point in P:
		if point != leftmost and point != rightmost:
			# Get the side of this particular point
			currSide = whichSide(leftmost, rightmost, point)

			# If it is not in the line L, and it is on the top of L
			if currSide != 0 and np.sign(topSide) == np.sign(currSide):
				topP.append(point)
			else:
				bottomP.append(point)

	# Initialize call to find Hull in the top and bottom section respectively
	topH = FindHull(topP, leftmost, rightmost)
	bottomH = FindHull(bottomP, rightmost, leftmost)

	# Merge final answer
	CH += [leftmost] + topH + bottomH + [rightmost]

# For a line X that passes through leftmost point to rightmost point
# This function searches for the farthest point P
# then recursively divide point thats located on the top side of line that passes through leftmost point to P 
# and recursively divide point thats located on the top side of line that passes through P to rightmost point 
def FindHull(P, leftmost, rightmost):
	# If theres no more point
	if len(P) == 0:
		# return empty set of point
		return []
	else:
		# Initialize distance to -1 as distance cant be negative 
		currMaxDist = -1
		# Precalculate distance of leftmost point to rightmost point
		distLR = distPTP(leftmost, rightmost)

		for point in P:
			# Calculate distance of particular point to the line
			pointDist = distPTL(leftmost, rightmost, point, distLR)
			currMaxDist = max(currMaxDist, pointDist)
			# Getting farthest point
			if currMaxDist == pointDist:
				currP = point

		# Initialize list of Hull in this section
		listofHull = [currP]

		# Getting all point with farthest distance
		for point in P:
			pointDist = distPTL(leftmost, rightmost, point, distLR)
			if currMaxDist == pointDist:
				listofHull.append(point)

		# Divide set of points into 2 sections
		topP = []
		botP = []

		# Getting the value of side
		sideRightmost = whichSide(leftmost, currP, rightmost)
		sideLeftmost = whichSide(currP, rightmost, leftmost)


		for point in P:
			if point not in listofHull:
				# For every point
				# Determine if it is in the inside of triangle
				# or in top side of line from leftmost point to farthest point
				# or in the top side of line from farthest to rightmost point
				l = whichSide(leftmost, currP, point)
				r = whichSide(currP, rightmost, point)
				if np.sign(l) != np.sign(sideRightmost):
					topP.append(point)
				if np.sign(r) != np.sign(sideLeftmost):
					botP.append(point)

		# Recursively find Hull from both sections
		topHull = FindHull(topP, leftmost, currP)
		bottomHull = FindHull(botP, currP, rightmost)
		return listofHull + topHull + bottomHull

if __name__ == "__main__":

	# Clearing screen for clarity
	os.system("cls")

	# Getting number of points
	nPoint = int(input("Number of points: "))

	# Getting maximum value of X and Y
	maxP = int(input("Maximum value of point: "))

	# Randomly generate X and Y
	genX = [x for x in [np.random.random_integers(0, maxP) for _ in range(nPoint)]]
	genY = [x for x in [np.random.randint(0, maxP) for _ in range(nPoint)]]

	# Merge X and Y together
	P = [[item[0], item[1]] for item in zip(genX, genY)] 
	
	# Container for Hulls
	ans = []

	# Initialize QuickHull
	solveQH(P, ans)

	# Getting centre point of Hulls
	centre = getCentre(ans)

	# Sorting hulls for plotting
	ans.sort(key = lambda x : (atan2(x[1]-centre[1], x[0]-centre[0])))

	# Separate X and Y because plt.plot() takes X and Y as separated arguments 
	ansX, ansY = [x for x in zip(*ans)]
	ansX = list(ansX)
	ansY = list(ansY)

	# Add the first point to the last sequence so that it becomes cyclic graph
	ansX.append(ans[0][0])
	ansY.append(ans[0][1])

	# Output list of Hulls
	print("Sequence of Hulls:")
	for i in range(len(ans)-1):
		l = ans[i]
		r = ans[i+1]
		if l != r:
			print("From {:>10} to {:}".format(str(ans[i]), str(ans[i+1])))

	# Plot all points as green circle
	plt.plot(genX, genY, "go")

	# Plot hulls as red circle and lines
	plt.plot(list(ansX), list(ansY), "ro-")

	# Shows the graph
	plt.show()

