#f1 = open('rooms-times-test.txt')

def converttominutes(time):
	#given a time, xx:xx, finds its value in minutes
	h,m = time.split(':')
	h, m = 60*int(h), int(m)
	return h+m

def converttoclock(n):
	h = str(n/60).zfill(2)
	m = str(n%60).zfill(2)
	return '%s:%s' %(h,m)

ALLSTARTTIMES, ALLENDTIMES, ALLDAYS = [], [], ['M', 'T', 'W', 'Th', 'F']

for i in xrange(8,22):
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':00'))
	ALLSTARTTIMES.append(converttominutes(str(i).zfill(2) + ':30'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':20'))
	ALLENDTIMES.append(converttominutes(str(i).zfill(2) + ':50'))
ALLTIMES = [[i,j,day] for i in ALLSTARTTIMES for j in ALLENDTIMES for day in ALLDAYS if j - i != 20 and j - i < 421]

room = 'PHY 150'
derp = []

freetimes, bookedtimes = {}, {}
for l in f1:
	room,time = l.split(',')
	time = time.strip().split(' ')
	starttime, endtime, day = converttominutes(time[0].split('-')[0]), converttominutes(time[0].split('-')[1]), time[1]
	#starttime, endtime, day = time[0].split('-')[0], time[0].split('-')[1], time[1]
	if starttime < 480:
		starttime = starttime + 12*60
	if endtime < 480:
		endtime = endtime + 12*60
	time = [starttime, endtime, day]
	if room not in bookedtimes:
		bookedtimes[room] = [time]
	else:
		bookedtimes[room].append(time)

print bookedtimes

"""
for l in f1:

	if room in l:
		derp.append(l.strip().split(', ')[1])
	a = [i.strip() for i in l.replace('-', ',').replace(' ', ',').split(',') if i.strip() != '']


shit = []
for i in derp: 
	if 'W' in i: print i
"""