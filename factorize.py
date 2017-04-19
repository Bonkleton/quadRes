#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  factorize.py
#  
#  Copyright 2017 Jesse Rominske
#  
#  Functions to print the prime power factorization of n

import math

# returns primality of i
def isPrime(i, primes):
	for p in primes:
		if p <= math.sqrt(i):
			if i % p == 0: return False
		else: return True

# produces a list of all primes up to the size of the square root of n
def generatePrimes(n):
	primes = [2]
	bound = int(math.ceil(math.sqrt(n) + 1))
	for i in range(3, bound):
		if isPrime(i, primes):
			primes.append(i)
	return primes

# produces a list of the factors of n
def checkFactors(n, primes):
	factors = []
	for p in primes:
		while n % p == 0:
			factors.append(p)
			n /= p
	if n > 1: factors.append(n) # larger than all p, so the list is still sorted
	return factors

# return the prime factors of n (as a list of integers)
def factorize(n):
	return sorted(list(set(checkFactors(n, generatePrimes(n)))))
