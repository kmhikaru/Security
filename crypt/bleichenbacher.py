# -*- coding: utf-8 -*-

studentNum = '16c01234'

def get_ST10(sn):
	tmp = int('0x'+sn,16)
	print "s(10) : " + str(tmp)
	print "ST(16): " + hex(tmp*(16**8))
	return tmp*(16**8)

def get_a10(sn):
	st = get_ST10(sn)
	a = 2**80 - st
	fr = a % 3
	M = st + fr
	a = a - fr
	print "FR(16): "+ hex(fr)
	print "M(16): " + hex(M)
	print "a(16): " + hex(a)
	return a

def main(sn):
	a = get_a10(studentNum)
	sig = 2**395 - (a/3)*(2**42)
	print "sig(16): " + hex(sig)
	print "sig**3(16): " + hex(sig**3)


'''	fr = b
	chk = 2**32
	while fr > chk:
		fr -=3
		print fr
	return fr
'''
main(studentNum)
