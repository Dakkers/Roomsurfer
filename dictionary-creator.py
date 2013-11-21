import json
FILE = open('raw1139times.txt')
DICTSFILES = open('fall2013times.txt', 'w')
"""
This program is not meant to be used for room checking. It is only meant to be used
to create the several dictionaries required for checking rooms. The dictionaries that
are created are explicitly put in their own Python file.
"""

ALLSTARTTIMES, ALLENDTIMES, ALLDAYS = [], [], ['M', 'T', 'W', 'Th', 'F']
def converttominutes(time):
	#given a time, xx:xx, finds its value in minutes
	h,m = time.split(':')
	h, m = 60*int(h), int(m)
	return h+m

def converttoclock(n):
	#given a number of minutes, converts the number to 'xx:xx' (24-hour clock)
	h = str(n/60).zfill(2)
	m = str(n%60).zfill(2)
	return '%s:%s' %(h,m)



for i in xrange(8,22):
	#generate all possible start and end times
	if i != 8:
		#avoid 8:00AM - xx:xx classes - they don't exist, except for that one time...
		ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':00'))
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':30'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':20'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':50'))
ALLTIMES = [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i < 540 and j - i > 0]
#combine all starttimes/endtimes on all days - avoid 20 minute classes and anything over 7 hours
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
			times.pop() #the previous time that was added must have been the 'T' in Th
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
					#if bt[0] in xrange(pt[0],pt[1]+10,10) or bt[1] in xrange(pt[0],pt[1]+10,10) or pt[0] in xrange(bt[0],bt[1]+10,10) or pt[1] in xrange(bt[0],bt[1]+10,10):
					#if start-bt is greater than start-pt or end-bt is less than end-pt
					#(i.e. the bt is completely or partially contained within the pt)
					#or if the pt is completely or partially contained within the bt, remove this time from the freetimes
					freetimes[room].remove(pt)
					n = n-1
				else:
					i=i+1
			else:
				i=i+1
				continue


for room in bookedtimes.keys():
	#the lab sections caused there to be duplicates of bookedtimes - get rid of those
	bookedtimes[room] = list(set([tuple(i) for i in bookedtimes[room]]))
for room in freetimes.keys():
	freetimes[room] = [tuple(i) for i in freetimes[room]]


"""
#convert all times from minutes to a 24-hour clock
for room in freetimes.keys():
	temp = []
	for l in freetimes[room]:
		converted = '%s-%s %s' %(converttoclock(l[0]), converttoclock(l[1]), l[2])
		#print l, converted
		temp.append(converted)
	freetimes[room] = temp

for room in bookedtimes.keys():
	temp = []
	for l in bookedtimes[room]:
		converted = '%s-%s %s' %(converttoclock(l[0]), converttoclock(l[1]), l[2])
		temp.append(converted)
	bookedtimes[room] = temp
"""

dicttowrite = {'bookedtimes': bookedtimes, 'freetimes': freetimes}
json.dump(dicttowrite, DICTSFILES)
