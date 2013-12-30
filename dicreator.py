import json
FILE = open('raw1141times.txt')
DICTSFILES = open('1141times.json', 'w')
"""
This program is not meant to be used for room checking. It is only meant to be used
to create the dictionary required for checking rooms. The dictionary that is 
created is put into a JSON file.
"""

ALLSTARTTIMES, ALLENDTIMES, ALLDAYS = [], [], ['M', 'T', 'W', 'Th', 'F']
def converttominutes(time):
	#given a time, xx:xx, finds its value in minutes
	h,m = time.split(':')
	h, m = 60*int(h), int(m)
	return h+m

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
	#given a list of lists, sorts the lists by the list's first element (small to large)
	if len(L) == 0 or len(L) == 1:
		return L
	d = {str(l[0]): l for l in L}
	mins = [int(i) for i in d.keys()]
	mins.sort()
	return [d[str(key)] for key in mins]


for i in xrange(8,22):
	#generate all possible start and end times
	if i != 8:
		#avoid 8:00AM - xx:xx classes - they don't exist, except for that one time...
		ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':00'))
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':30'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':20'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':50'))
ALLTIMES = [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i < 540 and j - i > 0]
#combine all starttimes/endtimes on all days - avoid 20 minute classes and anything over 8 hours
#also, generating all possible start/endtimes caused times such as 6:30 PM - 8:30 AM; ignore those



"""This section is for getting the booked times."""
freetimes, bookedtimes = {}, {}
for l in FILE:
	room,time = l.split(',')
	time = time.strip().split(' ')
	if len(time) == 2:
		starttime, endtime, day = converttominutes(time[0].split('-')[0]), converttominutes(time[0].split('-')[1]), time[1]
	else:
		starttime, endtime, day = converttominutes(time[0].split('-')[0]), converttominutes(time[0].split('-')[1]), time[2]

	#anything less than 08:00 is assumed to be in the evening - shift by 12 hours as the latest start time is 7 PM
	if endtime < 480 or starttime < 480:
		endtime = endtime + 12*60
	if starttime < 480:
		starttime = starttime + 12*60

	times = []
	for letter in day:
		#get each time as individual days
		if letter == 'h':
			times.pop() #the previous time that was added must have been the 'T' in Th - remove it
			times.append([starttime, endtime, 'Th']) #properly add Th
		else:
			times.append([starttime, endtime, letter])

	for time in times:
		if room not in bookedtimes:
			bookedtimes[room] = [time]
		else:
			bookedtimes[room].append(time)



"""This section is for getting the free times."""
for room in bookedtimes:
	#going through each room - assume that the room is always free
	freetimes[room] = [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i < 540 and j - i > 0]

	for bt in bookedtimes[room]:
		#for the room, let's look at all of its booked times

		i,n = 0,len(freetimes[room])
		while i < n:
			pt = freetimes[room][i]

			if pt[2] == bt[2]:
				if (pt[1] >= bt[0] >= pt[0]) or (pt[0] <= bt[1] <= pt[1]) or (bt[0] <= pt[0] <= bt[1]) or (bt[0] <= pt[1] <= bt[1]):
					#if start-bt is greater than start-pt or end-bt is less than end-pt (i.e. the bt is completely or partially contained within the pt)
					#or if the pt is completely or partially contained within the bt, remove this time from the freetimes
					freetimes[room].remove(pt)
					n = n-1
				else:
					i=i+1
			else:
				i=i+1
				continue



"""Clean up a bit."""
for room in bookedtimes.keys():
	#the lab sections caused there to be duplicates of bookedtimes - get rid of those
	bookedtimes[room] = list(set([tuple(i) for i in bookedtimes[room]]))

freetimes_sorted = dict(freetimes) #make a copy of freetimes
for room in freetimes_sorted.keys():
	#this will organize the freetimes for each room by day
	M,T,W,Th,F = [],[],[],[],[]
	for t in freetimes_sorted[room]:
		if 'M' in t: M.append([t[0],t[1]])
		elif 'T' in t: T.append([t[0], t[1]])
		elif 'W' in t: W.append([t[0], t[1]])
		elif 'Th' in t: Th.append([t[0], t[1]])
		else: F.append([t[0], t[1]])
	freetimes_sorted[room] = {'M': M, 'T': T, 'W': W, 'Th': Th, 'F': F}

for room in freetimes_sorted:
	for day in freetimes_sorted[room].keys():
		#clean up lists... a lot
		X = remove_subsets([xrange(l[0],l[1]+10,10) for l in freetimes_sorted[room][day]])
		L = [[l[0], l[-1]] for l in X]
		freetimes_sorted[room][day] = sorter(mergeify(L))

"""Create a dictionary with each key being a possible freetime, and its value being all the rooms free at that time."""
d = {}
for t in [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i > 0]:
	d[','.join([str(i) for i in t])] = [room for room in freetimes.keys() if t in freetimes[room]]
	d[','.join([str(i) for i in t])].sort()

dicttowrite = {'freerooms': d, 'freetimes_sorted': freetimes_sorted}
json.dump(dicttowrite, DICTSFILES)