'''this file is only here to test the json files
without creating them - that takes a while and I am
not a patient person... well it doesn't take that 
long, but too bad.'''

import json
a = json.load(open('fall2013times.txt'))
bookedtimes, freetimes = a['bookedtimes'], a['freetimes']

def remove_subsets(L):
	#traverses through a list of lists, removing lists that are subsets of others
	#all hail StackOverflow
	L2 = L[:]
	for m in L:
		for n in L:
			if set(m).issubset(set(n)) and m != n:
				L2.remove(m)
				break

	return L2

def mergeify(L):
	#this will remove subsets and partial subsets; 8:30-10:20,9:30-10:20 becomes 8:30-10:20
	#and 8:30-10:30,9:30-11:00 becomes 8:30-11:00
	L_return = []
	for m in L:
		temp, mxrange = range(m[0],m[1]+10,10), xrange(m[0],m[1]+10,10)
		for n in L:
			if any(x in xrange(n[0],n[1]+10,10) for x in mxrange) and m != n:
				temp += range(n[0],n[1]+10,10)
		temp = list(set(temp))
		temp.sort()
		L_return.append(tuple(temp))

	return [[l[0], l[-1]] for l in  list(set(L_return))]

def sorter(L):
	#given a list of lists, sorts the lists by the list's first element (int - small to large)
	if len(L) == 0 or len(L) == 1:
		return L
	d = {str(l[0]): l for l in L}
	mins = d.keys()
	mins.sort()
	return [d[key] for key in mins]


for room in freetimes.keys():
	M,T,W,Th,F = [],[],[],[],[]
	for t in freetimes[room]:
		if 'M' in t: M.append([t[0],t[1]])
		elif 'T' in t: T.append([t[0], t[1]])
		elif 'W' in t: W.append([t[0], t[1]])
		elif 'Th' in t: Th.append([t[0], t[1]])
		else: F.append([t[0], t[1]])
	freetimes[room] = {'M': M, 'T': T, 'W': W, 'Th': Th, 'F': F}


freetimes_sorted = {'BMH 2703': dict(freetimes['BMH 2703'])}
#print freetimes_sorted

for room in freetimes_sorted:
	for day in freetimes_sorted[room].keys():
		X = remove_subsets([xrange(l[0],l[1]+10,10) for l in freetimes_sorted[room][day]])
		L = [[l[0], l[-1]] for l in X]
		freetimes_sorted[room][day] = sorter(mergeify(L))

print freetimes_sorted