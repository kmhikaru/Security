# -*- coding: utf-8 -*-

n = 402356052281678260410458688175817639652517
s1 = 53392076929729593163521995541491552949498
s2 = 315086365666030406050065184470485976218800
e = 3	

def gcd(a,b):
	if b == 0:
		return int(a)
	if a < b:
		return gcd(b,a)
	else:
		return gcd(b,a%b)

def aug_gcd(a,b):
	if b == 0:
		u = 1
		v = 0
	else:
		q = a / b
		r = a % b
		(u0,v0) = aug_gcd(b,r)
		u = v0
		v = u0 - q*v0

	return (u,v)

def main(N,sigma1,sigma2,E):
	q = gcd(N,abs(sigma1-sigma2))
	p = N/q
	print "p: %d" % p
	print "q: %d" % q 
	phiN = (p-1)*(q-1)
	d = aug_gcd(E,phiN)[0]
	if d < 0:
		d+=phiN
	print "d: %d" % d 
#	print (d*E) % phiN	

main(n,s1,s2,e)	
