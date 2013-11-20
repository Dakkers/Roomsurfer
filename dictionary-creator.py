FILE = open('rooms-times-test.txt')
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
	h = str(n/60).zfill(2)
	m = str(n%60).zfill(2)
	return '%s:%s' %(h,m)

ALLSTARTTIMES, ALLENDTIMES, ALLDAYS = [], [], ['M', 'T', 'W', 'Th', 'F']

for i in xrange(8,22):
	#generate ALL possible times a room is being used - convert them all to minutes
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':00'))
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':30'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':20'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':50'))
ALLTIMES = [[i,j] for i in ALLSTARTTIMES for j in ALLENDTIMES if j - i != 20 and j - i < 421]
print len(ALLTIMES)

freetimes, bookedtimes = {}, {}
for l in FILE:
	room,time = l.split(',')
	time = time.strip().split(' ')
	starttime, endtime, day = converttominutes(time[0].split('-')[0]), converttominutes(time[0].split('-')[1]), time[1]
	#starttime, endtime, day = time[0].split('-')[0], time[0].split('-')[1], time[1]
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

#print bookedtimes['DWE 1515']


"""
#I'm sorry.
for room in bookedtimes:
	#going through each room
	freetimes[room] = []

	for bookedtime in bookedtimes[room]:
		#for the room, let's look at all of its booked times

		for possibletime in ALLTIMES:
			#now let's look at all possible times ...
			print 

			if possibletime[2] in bookedtime[2]:
				#but only if the day of the possible time is one of the days of the booked time

				if bookedtime == possibletime:
					#if the bookedtime and a possible time are the same, skip past it
					continue

				elif bookedtime[0] >= possibletime[0] or bookedtime[1] <= possibletime[1]:
					#if start-bookedtime is greater than start-possibletime or end-bookedtime is less than end-possibletime
					#(i.e. the bookedtime is completely or partially contained within the possibletime) then skip past it
					continue

				else:
					freetimes[room].append(possibletime)

			else:
				continue

"""