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
def distPTL(A, B, P):
	print(A, B, P)
	numerator = abs(whichSide(A, B, P))
	denominator = hyp((B[1]-A[1]), (B[0]-A[0]))
	print(numerator, denominator)
	return numerator/denominator

# This function initializes recursive calls for finding hulls
def solveQH(P, CH):
	# Sorting set of points by X first, then by Y
	P.sort(key = lambda x : (x[0], x[1]))

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

	topH = FindHull(topP, leftmost, rightmost)
	bottomH = FindHull(bottomP, rightmost, leftmost)
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

		for point in P:
			# Calculate distance of particular point to the line
			pointDist = distPTL(leftmost, rightmost, point)
			currMaxDist = max(currMaxDist, pointDist)
			if currMaxDist == pointDist:
				currP = point

		listofHull = [currP]

		for point in P:
			pointDist = distPTL(leftmost, rightmost, point)
			if currMaxDist == pointDist:
				listofHull.append(point)

		topP = []
		botP = []
		sideRightmost = whichSide(leftmost, currP, rightmost)
		sideLeftmost = whichSide(currP, rightmost, leftmost)
		for point in P:
			# if point == currP:
			# 	continue
			# else:
			if point not in listofHull:
				l = whichSide(leftmost, currP, point)
				r = whichSide(currP, rightmost, point)
				if np.sign(l) != np.sign(sideRightmost):
					topP.append(point)
				if np.sign(r) != np.sign(sideLeftmost):
					botP.append(point)

		print("Ini LRMost dan currP", leftmost, currP, rightmost)
		print("Ini topP", topP)
		print("Ini botP", botP)
		tH = FindHull(topP, leftmost, currP)
		bH = FindHull(botP, currP, rightmost)
		print("Ini currP", currP, tH, bH)
		return listofHull + tH + bH

if __name__ == "__main__":
	os.system("cls")
	nPoint = int(input("Number of points: "))
	maxP = int(input("Maximum value of point: "))
	genX = [x for x in [np.random.random_integers(0, maxP) for _ in range(nPoint)]]
	genY = [x for x in [np.random.randint(0, maxP) for _ in range(nPoint)]]
	P = [[item[0], item[1]] for item in zip(genX, genY)] 
	ans = []
	solveQH(P, ans)
	centre = getCentre(ans)
	ans.sort(key = lambda x : (atan2(x[1]-centre[1], x[0]-centre[0])))
	# ans.append(ans[0])
	print(ans)
	ansX, ansY = [x for x in zip(*ans)]
	ansX = list(ansX)
	ansY = list(ansY)
	ansX.append(ans[0][0])
	ansY.append(ans[0][1])
	# print(list(ansX), list(ansY))
	plt.plot(genX, genY, "go")
	plt.plot(list(ansX), list(ansY), "ro-")
	# plt.plot(list(ansX), list(ansY), "r-")
	# plt.plot([1,2,3], [4,5,6], "ro")
	# ans = set(ans)
	for i in range(len(ans)-1):
		l = ans[i]
		r = ans[i+1]
		if l != r:
			print(ans[i], ans[i+1])
	plt.show()

