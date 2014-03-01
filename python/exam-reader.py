f = open('raw-1139examtimes.txt')
g = open('1139examtimes.txt', 'w')
alldays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
allsubs = ['AFM', 'ACTSC', 'ANTH', 'AHS', 'APPLS', 'AMATH', 'ARCH', 'ARTS', 'ARBUS', 'AVIA', 'BIOL', 'BUS', 'BET', 'CHE', 'CHEM', 'CHINA', 'CMW', 'CIVE',
			'CLAS', 'CO', 'COMM', 'CS', 'COOP', 'CROAT', 'DAC', 'DRAMA', 'DUTCH', 'EARTH', 'EASIA', 'ECON', 'ECE', 'ENGL', 'ESL', 'EFAS', 'ENBUS', 'ERS', 
			'ENVE', 'ENVS', 'FINE', 'FR', 'GENE', 'GEOG', 'GEOE', 'GER', 'GERON', 'GBDA', 'GRK', 'HLTH', 'HIST', 'HRM', 'HUMSC', 'IS', 'INDEV', 'INTST', 
			'INTTS', 'ITAL', 'ITALST', 'JAPAN', 'JS', 'KIN', 'INTEG', 'KOREA', 'LAT', 'LS', 'MATBUS', 'MSCI', 'MNS', 'MATH', 'MTHEL', 'ME', 'MTE', 'MEDVL',
			'MUSIC', 'NE', 'NATST', 'OPTOM', 'PACS', 'PHARM', 'PHIL', 'PHYS', 'PLAN', 'POLSH', 'PSCI', 'PORT', 'PD', 'PDPHRM', 'PSYCH', 'PMATH', 'REC', 'RS',
			'RUSS', 'REES', 'SCI', 'SCBUS', 'SMF', 'SDS', 'SOCWK', 'SWREN', 'STV', 'SOC', 'SE', 'SPAN', 'SPCOM', 'STAT', 'SI', 'SYDE', 'UNIT', 'VCULT', 'WS',
			'WKRPT']
allbuildings = ['AAR', 'ACW', 'AL', 'ARC', 'B1', 'B2', 'BAU', 'BMH', 'BRH', 'C2', 'CGR', 'CIF', 'CLN', 'CLV', 'COG', 'COM', 'CPH', 'CSB', 'DC', 'DWE', 'E2',
				'E3', 'E5', 'E6', 'ECH', 'EIT', 'ERC', 'EV1', 'EV2', 'EV3', 'ESC', 'FED', 'GA', 'GH', 'GSC', 'HH', 'HMN', 'HS', 'HSC', 'IHB', 'KDC', 'LHI', 
				'LIB', 'M3', 'MC', 'MHR', 'MKV', 'ML', 'NH', 'OPT', 'PAC', 'PAS', 'PHR', 'PHY', 'QNC', 'RA2', 'RAC', 'RCH', 'REN', 'REV', 'SCH', 'SLC',
				'STJ', 'STP', 'TC', 'TH', 'UAE', 'UC', 'UWP', 'V1', 'WSS']

examtimes = []
conditions  = ("Exam removed from the schedule", "On Line", "See http://www.wlu.ca/page.php?grp_id=1366&p=14566 WLU")

for l in f: 
	ideal = l.replace('Fall 2013', '').replace(' to ', ',')

	if any(con in ideal for con in conditions):
		#ignore all exams removed from schedules, all online courses and all WLU-based exams
		continue

	if any(building in ideal for building in allbuildings) or any(sub in ideal for sub in allsubs):
		#ignore all 'Fall 2013', 'Final Examination Schedule', etc. lines which occur on each page
		examtimes.append(ideal)

"""
Okay so we have all exam times, but we also have some lines that just have rooms in them due to the fact that
too many exam locations for one course spills over into a newline in the exam pdf - take care of that. The way 
to check if the string is just for rooms is by seeing if 'December' is in it. Generally there's only one extra 
line of rooms, but for CHEM 120, there are two - however, all of the rooms appear on new lines (3 extra lines).
Thus, I check for three, two, and one extra line(s) respectively.
"""
i, properexamtimes = 0, []
while i < len(examtimes):
	
	try:
		#it'll error when it gets to the last one, could use another if statement but whatever

		if 'December' not in examtimes[i+1] and 'December' not in examtimes[i+2] and 'December' not in examtimes[i+3]:
			#handle CHEM 120 in particular... fuck.
			s = '%s %s,%s,%s'.replace(',,', ',') %(examtimes[i].strip(),examtimes[i+1].strip(),examtimes[i+2].strip(),examtimes[i+3])
			s = s.replace(',,', ',')
			i = i + 4

		elif 'December' not in examtimes[i+1] and 'December' not in examtimes[i+2]:
			s = '%s,%s,%s'.replace(',,', ',') %(examtimes[i].strip(),examtimes[i+1].strip(),examtimes[i+2])
			s = s.replace(',,', ',')
			i = i + 3

		elif 'December' not in examtimes[i+1]:
			s = '%s,%s' %(examtimes[i].strip(), examtimes[i+1])
			s = s.replace(',,', ',')
			i = i + 2

		else:
			s = examtimes[i]
			i = i + 1

		s = s.split(' ')[2:]
		properexamtimes.append(s)

	except:
		i = i + 1

for s in properexamtimes:
	i = s.index('December')
	date, starttime, endtime, rooms = s[i+1], "%s %s"% (s[i+3],s[i+4]), "%s %s"% (s[i+5],s[i+6]), ' '.join(s[i+7:]).strip()
	print rooms