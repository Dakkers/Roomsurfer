import json
FILE = open('raw1139times.txt')
DICTSFILES = open('fall2013times.txt', 'w')
"""
This program is not meant to be used for room checking. It is only meant to be used
to create the several dictionaries required for checking rooms. The dictionaries that
are created are explicitly put in their own Python file.
"""

def converttominutes(time):
	#given a time, xx:xx, finds its value in minutes
	h,m = time.split(':')
	h, m = 60*int(h), int(m)
	return h+m

def converttoclock(n):
	#given a number of minutes, converts the number to 'xx:xx' (24-hour clock)
	if n >= 780:
		n = n - 720
	h = str(n/60).zfill(2)
	m = str(n%60).zfill(2)
	return '%s:%s' %(h,m)

ALLSTARTTIMES, ALLENDTIMES, ALLDAYS = [], [], ['M', 'T', 'W', 'Th', 'F']

for i in xrange(8,22):
	#generate all possible start and end times
	if i != 8:
		#avoid 8:00AM - xx:xx classes - they don't exist, except for that one time...
		ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':00'))
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':30'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':20'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':50'))
ALLTIMES = [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i < 421 and j - i > 0]
#combine all starttimes/endtimes on all days - avoid 20 minute classes and anything over 7 hours
#also, generating all possible start/endtimes caused times such as 6:30 PM - 8:30 AM; ignore those

freetimes, bookedtimes = {}, {}
for l in FILE:
	room,time = l.split(',')
	time = time.strip().split(' ')
	starttime, endtime, day = converttominutes(time[0].split('-')[0]), converttominutes(time[0].split('-')[1]), time[1]
	#starttime, endtime, day = time[0].split('-')[0], time[0].split('-')[1], time[1]

	#anything less than 08:00 is assumed to be in the evening - shift by 12 hours
	if starttime < 480:
		starttime = starttime + 12*60
	if endtime < 480:
		endtime = endtime + 12*60

	times = []
	for letter in day:
		if letter == 'h':
			times.pop()
			times.append([starttime, endtime, 'Th'])
		else:
			times.append([starttime, endtime, letter])

	for time in times:
		if room not in bookedtimes:
			bookedtimes[room] = [time]
		else:
			bookedtimes[room].append(time)

#json.dump(bookedtimes, DICTSFILES)

for room in bookedtimes:
	#going through each room - assume that the room is always free
	freetimes[room] = ALLTIMES

	for btime in bookedtimes[room]:
		#for the room, let's look at all of its booked times

		for ptime in ALLTIMES:
			#now let's look at all possible times ...

			if ptime[2] == btime[2]:
				#but only if the days are the same

				if (ptime[1] >= btime[0] >= ptime[0]) or (ptime[0] <= btime[1] <= ptime[1]) or (btime[0] <= ptime[0] <= btime[1]):
					#if start-btime is greater than start-ptime or end-btime is less than end-ptime
					#(i.e. the btime is completely or partially contained within the ptime)
					#or if the ptime is completely or partially contained within the btime, remove this time from the freetimes
					freetimes[room].remove(ptime)

dicttowrite = {'bookedtimes': bookedtimes, 'freetimes': freetimes}
json.dump(dicttowrite, DICTSFILES)