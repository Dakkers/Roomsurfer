import json
a = json.load(open('fall2013times.txt'))
bookedtimes, freetimes = a['bookedtimes'], a['freetimes']

def mergeify(L):
	#given a list of lists, L, all lists that are subsets of other lists are removed
	#yes I stole this from StackOverflow, deal with it
	Lcopy = L[:]
	for m in L:
		for n in L:
			if set(m).issubset(set(n)) and m != n:
				Lcopy.remove(m)
				break
	return Lcopy


for room in freetimes.keys():
	M,T,W,Th,F = [],[],[],[],[]
	for t in freetimes[room]:
		if 'M' in t: M.append([t[0],t[1]])
		elif 'T' in t: T.append([t[0], t[1]])
		elif 'W' in t: W.append([t[0], t[1]])
		elif 'Th' in t: Th.append([t[0], t[1]])
		else: F.append([t[0], t[1]])
	freetimes[room] = {'M': M, 'T': T, 'W': W, 'Th': Th, 'F': F}


freetimes_sorted = {'PHY 145': dict(freetimes['PHY 145']), 'PHY 150': dict(freetimes['PHY 150'])}
print freetimes_sorted
for room in freetimes_sorted:
	for day in freetimes_sorted[room].keys():
		X = mergeify([xrange(l[0],l[1]+10,10) for l in freetimes_sorted[room][day]])
		L = [[l[0], l[-1]] for l in X]
		freetimes_sorted[room][day] = L

print freetimes_sorted