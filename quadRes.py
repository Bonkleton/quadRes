#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  quadRes.py
#  
#  Copyright 2017 Jesse Rominske <bonkie@ALTRON-UbuntuStudio>
#  
#  Finds R+-(a) where a is an odd integer

import math
import sys
import factorize

# finds an inverse of a given mod m
def modInverse(a, m):
	i = 1
	for i in range(1, m):
		if (a * i) % m == 1:
			return i
	# the lines below will only execute if the loop finished and never returned i
	print("No inverse of " + str(a) + " mod " + str(m))
	return 1

# finds the quadratic residues and non-residues of a prime p
def quadResPrime(p):
	rPlus = set([])
	rMinus = set([])
	ints = set(range(1, p))
	for i in ints:
		x = (i * i) % p
		rPlus.add(x)
	print("r+(" + str(p) + ") = " + str(list(rPlus)))
	rMinus = ints - rPlus
	print("r-(" + str(p) + ") = " + str(list(rMinus)))
	
	# if congruent to 1 mod 4, we're done
	if p % 4 == 1:
		return rPlus, rMinus
	
	xPlus = set([])
	for r in rPlus:
		# apply Chinese Remainder Theorem
		y1 = modInverse(p, 4)
		y2 = modInverse(4, p)
		x = ((p * y1) + (r * 4 * y2)) % (4 * p)
		xPlus.add(x)
	xMinus = set([])
	for r in rMinus:
		# apply Chinese Remainder Theorem
		y1 = modInverse(p, 4)
		y2 = modInverse(4, p)
		x = (-(p * y1) + (r * 4 * y2)) % (4 * p)
		xMinus.add(x)
	
	RPlus = xPlus | xMinus
	RMinus = set([])

	factors = factorize.factorize(4 * p)
	# create set of relatively prime moduli not in R+
	for i in range(1, (4 * p)):
		legit = True
		for f in factors:
			if i % f != 0:
				continue
			else:
				legit = False
		if legit and i not in RPlus:
			RMinus.add(i)
	
	return RPlus, RMinus

# finds the quadratic residues and non-residues of an intenger a
# by finding those of its factors
def quadResInt(a):
	# handle negative numbers because factorize does not work with them,
	# and because they are fairly easy to handle anyway
	# we treat a as positive until the end
	isNegative = False
	if a < 0:
		isNegative = True
		a = -a
	
	factors1 = factorize.factorize(a)
	print("Factors of " + str(a) + ": " + str(factors1))
	RiPluses = []
	RiMinuses = []
	needs4a = False
	for f in factors1:
		RiPlus, RiMinus = quadResPrime(f)
		
		# here we associate each set of quadratic residues with its modulus
		# i.e., the set of quadtratic residues of 7 is passed in as [28, R+(7)]
		if f % 4 == 1:
			RiPluses.append([(f), RiPlus])
			RiMinuses.append([(f), RiMinus])
			print("R+(" + str(f) + ") = " + str(sorted(list(RiPlus))))
			print("R-(" + str(f) + ") = " + str(sorted(list(RiMinus))))
		else:
			needs4a = True
			RiPluses.append([(4 * f), RiPlus])
			RiMinuses.append([(4 * f), RiMinus])
			print("R+(" + str(4 * f) + ") = " + str(sorted(list(RiPlus))))
			print("R-(" + str(4 * f) + ") = " + str(sorted(list(RiMinus))))
	
	RPlus = set([])
	RMinus = set([])
	
	if needs4a:
		lim = 4 * a
	else:
		lim = a
		
	if isNegative:
		# R+(-1) & R+(5) & R+(7)
		for i in range(1, lim):
			if (i % 4 == 1) and (i % RiPluses[0][0] in RiPluses[0][1]) and (i % RiPluses[1][0] in RiPluses[1][1]):
				RPlus.add(i)
			else:
				continue
		# R+(-1) & R-(5) & R-(7)
		for i in range(1, lim):
			if (i % 4 == 1) and (i % RiPluses[0][0] in RiMinuses[0][1]) and (i % RiPluses[1][0] in RiMinuses[1][1]):
				RPlus.add(i)
			else:
				continue
		# R-(-1) & R+(5) & R-(7)
		for i in range(1, lim):
			if (i % 4 == 3) and (i % RiPluses[0][0] in RiPluses[0][1]) and (i % RiPluses[1][0] in RiMinuses[1][1]):
				RPlus.add(i)
			else:
				continue
		# R-(-1) & R-(5) & R+(7)
		for i in range(1, lim):
			if (i % 4 == 3) and (i % RiPluses[0][0] in RiMinuses[0][1]) and (i % RiPluses[1][0] in RiPluses[1][1]):
				RPlus.add(i)
			else:
				continue
	
	factors2 = factorize.factorize(4 * a)
	# create set of relatively prime moduli not in R+
	for i in range(1, lim):
		legit = True
		for f in factors2:
			if i % f != 0:
				continue
			else:
				legit = False
		if legit and i not in RPlus:
			RMinus.add(i)
					
	RPlus = sorted(list(RPlus))
	RMinus = sorted(list(RMinus))
	print("R+(" + str(-a) + ") = " + str(RPlus))
	print("R-(" + str(-a) + ") = " + str(RMinus))
	
	return RPlus, RMinus

# prints the result all pretty-like	
def printR(a, R, isPlus):
	if isPlus:
		message = "R+(" + str(a) + ") = {p:p congruent to 1,"
	else:
		message = "R-(" + str(a) + ") = {p:p congruent to "
	for r in R:
		if r == 1:
			continue
		message = message + str(r) + ","
	message = message + "mod " + str(4 * a) + "}"
	print(message)

# main program structure
def main(args):
	RPlus1, RMinus1 = quadResInt(29)
	printR(29, RPlus1, True)
	printR(29, RMinus1, False)
	
	RPlus2, RMinus2 = quadResInt(-35)
	printR(-35, RPlus2, True)
	printR(-35, RMinus2, False)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
