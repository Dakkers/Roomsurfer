import urllib
import urllib2
import string
from bs4 import BeautifulSoup
"""This script simply writes all of the times that a room is being used by
a lecture, lab, tutorial or whatever. It is not nearly perfect yet - there
are still some bugs taht need to be fixed. This script is not meant to be 
used to be found the times of the room, this is just for writing."""

F = open('raw1151times.txt', 'w')
allcoms = ['CLN','DIS','ENS','ESS','FLD','LAB','LEC','ORL','PRA','PRJ','RDG','SEM','STU','TLC','TST','TUT','WRK','WSP']
allsubs = ['AB', 'ACC', 'ACINTY', 'ACTSC', 'AFM', 'AHS', 'AMATH', 'ANTH', 'APPLS', 'ARBUS', 'ARCH', 'ARCHL', 'ARTS', 'ASTRN', 'AVIA', 'BASE',
			'BE', 'BET', 'BIOL', 'BME', 'BUS', 'CEDEV', 'CHE', 'CHEM', 'CHINA', 'CIVE', 'CLAS', 'CM', 'CMW', 'CO', 'COGSCI', 'COMM', 'COMST', 'CONST', 'COOP', 
			'CRGC', 'CROAT', 'CS', 'CT', 'CULT', 'DAC', 'DEI', 'DRAMA', 'DUTCH', 'EARTH', 'EASIA', 'ECE', 'ECON', 'EFAS', 'ELPE', 'EMLS', 'ENBUS', 'ENGL', 'ENVE', 
			'ENVS', 'ERS', 'ESL', 'FILM', 'FINE', 'FR', 'GBDA', 'GEMCC' 'GENE', 'GEOE', 'GEOG', 'GER', 'GERON', 'GGOV', 'GLOBAL', 'GRK', 
			'GS', 'HBIO', 'HIST', 'HLTH', 'HRM', 'HSG', 'HUMSC', 'INDEV', 'INTEG', 'INTERN', 'INTST', 'INTTS', 'IS', 'ITAL', 'ITALST', 'JAPAN', 'JS', 
			'KIN', 'KOREA', 'KPE', 'LANG', 'LAT', 'LED', 'LS', 'MATBUS', 'MATH', 'ME', 'MEDVL', 'MI', 'MISC', 'MNS', 'MSCI', 'MTE', 'MTHEL', 'MUSIC', 'NANO',
			'NATST', 'NE', 'NES', 'OPTOM', 'PACS', 'PHARM', 'PHIL', 'PHS', 'PHYS', 'PLAN', 'PMATH', 'PORT', 'PS', 'PSCI', 
			'PSYCH', 'QIC', 'REC', 'REES', 'RELC', 'RS', 'RSCH', 'RUSS', 'SCBUS', 'SCI', 'SDS', 'SE', 'SEQ', 'SI', 'SMF', 'SOC', 'SOCIN', 'SOCWK', 'SOCWL', 'SPAN',
			'SPCOM', 'STAT', 'STV', 'SUSM', 'SWK', 'SWREN', 'SYDE', 'TAX', 'TN', 'TOUR', 'TPM', 'TS', 'UN', 'UNIV', 'VCULT', 'WATER', 'WS']
alldays = ['Th', 'M', 'T', 'W', 'F']
allbuildings = ['AAR', 'ACW', 'AL', 'ARC', 'B1', 'B2', 'BAU', 'BMH', 'BRH', 'C2', 'CGR', 'CIF', 'CLN', 'CLV', 'COG', 'COM', 'CPH', 'CSB', 'DC', 'DWE', 'E2',
				'E3', 'E5', 'E6', 'ECH', 'EIT', 'ERC', 'EV1', 'EV2', 'EV3', 'ESC', 'FED', 'GA', 'GH', 'GSC', 'HH', 'HMN', 'HS', 'HSC', 'IHB', 'KDC', 'LHI', 
				'LIB', 'M3', 'MC', 'MHR', 'MKV', 'ML', 'NH', 'OPT', 'PAC', 'PAS', 'PHR', 'PHY', 'QNC', 'RA2', 'RAC', 'RCH', 'REN', 'REV', 'SCH', 'SLC',
				'STJ', 'STP', 'TC', 'TH', 'UAE', 'UC', 'UWP', 'V1', 'WSS']


term = "1151"
num = ""
for sub in allsubs:
	data = {"sess" : term, "subject" : sub, "cournum" : num}
	encoded_data = urllib.urlencode(data)
	content = urllib2.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl",	encoded_data)
	soup = BeautifulSoup(content.read())
	stuff = soup.find_all("td", align="center")
	if 'AL 6' in stuff: 
		print stuff
	l = [str(i.text).strip() for i in stuff]
	for fuck in l:
		if 'DC 3701' in fuck: 
			print l
			print '\n\n\n\n'


	classnum, numindex = [], []
	for i in xrange(len(l)):
		a = l[i]

		if len(a) == 4:
			"""This for-loop gets the indices of the class numbers. Why? Because there are multiple
			sections to a course, generally. It is possible to split up these sections based off of
			where the class numbers appear. Also, it gets the components (LEC 001, etc.) """
			try:
				#takes care of the possibility of something else being len4
				int(a)
				if any(com in l[i+1] for com in allcoms):	#check if next element is of the form COM ###
					numindex.append(i)
			except:
				pass

	classes = []
	for i in range(len(numindex)):
		#splits the class sections
		try:
			n1 = numindex[i]
			n2 = numindex[i+1]
			classes.append(l[n1:n2])
		except:
			#for the last class number
			n = numindex[i]
			classes.append(l[n:])


	timesrooms = []
	for c in classes:
		temp = []
		for i in c:

			try:
				#check to see if i is an int or float - if so, don't bother with it
				float(i)

			except:
				#if it is not a float or int, check if ':' is in it
				if (':' in i and '0' in i and '-' in i and 'v' not in i): #for times/day
					temp.append(i)
				elif any(b in i.split() for b in allbuildings) and any(str(n) in i for n in xrange(10)) and ':' not in i and 'v' not in i:
				#for room - all of those checks are there because they are cheap workarounds
					temp.append(' '.join(i.split()))

		timesrooms.append(temp)

	#remove empties and classes with no rooms (online, or reading classes)
	timesrooms = [l for l in timesrooms if len(l) != 0 and len(l) != 1 and any(b in l[1] for b in allbuildings)]


	#handle lab sections
	temp = []
	for l in timesrooms:
		n = len(l)

		if n == 2:
			temp.append(l)

		elif n == 3:
			temp.append([l[0], l[1]])
			temp.append([l[2], l[1]])

		else:
			#handles n >= 4
			if n%2 == 0:
				for i in xrange(0,n - 1, 2): 	#these are mostly for labs that only occur on certain dates
					temp.append([l[i], l[i+1]])
	timesrooms = [l for l in temp]
	#reverse time/room to room/time
	timesrooms = [i[::-1] for i in timesrooms]

	# remove all lists that don't have any building names in them - this happens due to TST sections
	i,n = 0,len(timesrooms)
	while i < n:
		l = timesrooms[i]
		if not any(b in l[0] for b in allbuildings):
			timesrooms.remove(l)
			n=n-1
		else:
			i=i+1

	#separate and write
	for l in timesrooms:
		room = l[0]

		try:
			starttime, endtime = l[1].split('-')
			days = ''.join([i for i in endtime if (i in string.lowercase or i in string.uppercase)])
			endtime = ''.join([i for i in endtime if (i not in string.lowercase and i not in string.uppercase)])
			L = [room, "%s-%s %s" %(starttime, endtime, days)]

		except:
			stuff = l[1].split('-')
			starttime = stuff[0]
			days = ''.join([i for i in stuff[1] if (i in string.lowercase or i in string.uppercase)])
			endtime = stuff[1][:5]
			date = stuff[1][-5:]
			L = [room, "%s-%s %s %s" %(starttime, endtime, date, days)]

		F.write(', '.join(L) + "\n")