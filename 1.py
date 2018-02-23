# =============================
# Libraries
# =============================
import numpy as np
import matplotlib.pyplot as plt
from math import hypot as hyp
from copy import deepcopy as dcopy
import random
import os
import functools 
import math
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

# For a line L that passes through a point A to point B
# This function determines on which side of L is P located 
def whichSide(A, B, P):
	return (P[0]-A[0])*(B[1]-A[1]) - (P[1]-A[1])*(B[0]-A[0])

# For a line L that passes through a point A to point B
# This function returns the perpendicular distance from P to L
def distPTL(A, B, P):
	print(A, B, P)
	numerator = abs(whichSide(A, B, P))
	denominator = hyp((B[1]-A[1]), (B[0]-A[0]))
	print(numerator, denominator)
	return numerator/denominator

def solveQH(P, CH):

	# This variable contains points of Hull
	# CH = []

	# Sorting set of points
	P.sort(key = lambda x : (x[0], x[1]))

	# Finding leftmost point, rightmost point
	# Lets say L is line drawn from leftmost point to rightmost point
	# A random point located at the top of the line L is needed to determine on which side of the line L that a point is located
	leftmost = P[0]
	rightmost = P[-1]
	aTopPoint = [leftmost[0], leftmost[1]+1]
	dTop = whichSide(leftmost, rightmost, aTopPoint)

	topP = []
	bottomP = []
	for point in P[1:-1]:
		print("Ini point yang mau dicari", point)
		t = whichSide(leftmost, rightmost, point)
		# b = whichSide(rightmost, leftmost, point)
		if t != 0 and np.sign(dTop) == np.sign(t):
			topP.append(point)
		else:
			bottomP.append(point)

	# print("Ini P, topP, botP", P, topP, bottomP)
	print("Ini P", P)
	print("Ini topP", topP)
	print("Ini bottomP", bottomP)
	topH = FindHull(topP, leftmost, rightmost)
	bottomH = FindHull(bottomP, rightmost, leftmost)
	print("Ini topH dan botH", topH, bottomH)
	CH += [leftmost] + topH + bottomH + [rightmost]

def FindHull(P, leftmost, rightmost):
	if len(P) == 0:
		return []
	else:
		currMinDist = -1
		for point in P:
			pointDist = distPTL(leftmost, rightmost, point)
			currMinDist = max(currMinDist, pointDist)
			if currMinDist == pointDist:
				currP = dcopy(point)
		topP = []
		botP = []
		ltop = []
		ltop = rightmost
		rtop = leftmost
		# rtop = [rightmost[0]+1, rightmost[1]+1]
		dlTop = whichSide(leftmost, currP, ltop)
		drTop = whichSide(currP, rightmost, rtop)
		for point in P:
			if point == currP:
				continue
			else:
				l = whichSide(leftmost, currP, point)
				r = whichSide(currP, rightmost, point)
				if l != 0 and np.sign(l) != np.sign(dlTop):
					topP.append(point)
				if r != 0 and np.sign(r) != np.sign(drTop):
					botP.append(point)

		print("Ini LRMost dan currP", leftmost, currP, rightmost)
		print("Ini topP", topP)
		print("Ini botP", botP)
		tH = FindHull(topP, leftmost, currP)
		bH = FindHull(botP, currP, rightmost)
		print("Ini currP", currP, tH, bH)
		return [currP] + tH + bH

if __name__ == "__main__":
	os.system("cls")
	nPoint = int(input("Number of points: "))
	maxP = int(input("Maximum value of point: "))
	# genX = [item for item in np.random.randint(0, maxP, nPoint)]
	# genY = [item for item in np.random.randint(0, maxP, nPoint)]
	genX = [x for x in [random.randint(0, maxP) for _ in range(nPoint)]]
	genY = [x for x in [random.randint(0, maxP) for _ in range(nPoint)]]
	# print(genX)
	# print(genY)
	# genY = rand(0, maxP, nPoint)
	P = [[item[0], item[1]] for item in zip(genX, genY)] 
	# print(P)
	ans = []
	solveQH(P, ans)
	centre = getCentre(ans)
	ans.sort(key = lambda x : (math.atan2(x[1]-centre[1], x[0]-centre[0])))
	# ans.append(ans[0])
	print(ans)
	ansX, ansY = [x for x in zip(*ans)]
	ansX = list(ansX)
	ansY = list(ansY)
	ansX.append(ans[0][0])
	ansY.append(ans[0][1])
	print(list(ansX), list(ansY))
	plt.plot(genX, genY, "bo")
	plt.plot(list(ansX), list(ansY), "ro")
	plt.plot(list(ansX), list(ansY), "r-")
	# plt.plot([1,2,3], [4,5,6], "ro")
	plt.show()

