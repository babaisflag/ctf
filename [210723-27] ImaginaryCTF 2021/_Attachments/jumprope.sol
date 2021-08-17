val = 2
dead = 0
count = 0
x = <some big bytestring>

def test(a):	// test if prime; return 1 if prime, return 0 if composite
	if (a != 1):
		vc = 2
		while (vc < a-1):
			if (a % vc != 0):
				vc++
			else:
				return 0
		return 1
	return 0

def next(val):
	for(c = 0; c <= 7; c++):
		v18 = 0
		v20 = val
		for(i = 0; i <= 7; i++):
			a = i+1
			if(test(a) != 0):
				a = v20
				a &= 1
				v18 ^= a
			v20 = v20 >> 1
		val = val >> 1
		a = v18 << 7
		val += a
	return val
	
def checkflag():
	&ret = rbp+8;
	scanf("%88s%c", &ret, &dead)
	count = 8
	for (; count <= 95; count++):
		val = next(val)
		ecx= *(char*)(rbp+count)	// our input
		rdx = x[(count-8)*8] // indexed by bytes
		edx = val^edx^ecx
		*(rbp+count) = edx
	return 0
	
our input: result ^ x ^ val

val = 	0x854df0680d917b31cb38d595f4e7db81c22678b486c8bd98659cea4afaf3ed4061133c5a43e45ecc324e7525fdf976a0b0091ead21722f6619a7ba92fe7c3b50d8048fd610b917b38c535d497fbe1d286c82476b88dc8b59
x = 	0xfd3cc40e76ff4b451f40f4e680b8b5e8768e3bf8e4bdc9c73fe6cf15949a8a284e5e1e3f25d42ca936284240938d0fffae2b2bdf7e1a4e0563d088e1a11f5a3d364fae897bd727d029c09ef020df697794e9580fb8ecf924
res = 	0x11124000000000008b14400000000000d3c03713000000002e124000000000005b124000000000005b12400000000000781240000000000011124000000000008b14400000000000cefaadde000000009512400000000000
inp = 	0x696374667b6e30745f6c6173745f6e696768745f6275745f7468655f6e696768745f6265663072655f7477656e74795f663075725f6861636b6572735f63616d655f615f6b6e30636b696e675f61745f6d795f643030727d