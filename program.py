`import urllib
import urllib2
import string
from bs4 import BeautifulSoup
"""Eventually, this program will be designed to scrape the University of Waterloo's 
schedule of classes for undergraduate students after being given input from the user 
in order to create a schedule for the user.

The program is NOT meant to handle enrolment of any kind, as that is done through 
Quest, so all numbers related to that, such as enrolment cap, enrolment total, wait 
cap, wait total and reservation numbers are discarded. Also, associated class and 
related component numbers are discarded too."""

allcoms = ['CLN','DIS','ENS','ESS','FLD','LAB','LEC','ORL','PRA','PRJ','RDG','SEM','STU','TLC','TST','TUT','WRK','WSP']
allsubs = ['AFM', 'ACTSC', 'ANTH', 'AHS', 'APPLS', 'AMATH', 'ARCH', 'ARTS', 'ARBUS', 'AVIA', 'BIOL', 'BUS', 'BET', 'CHE', 'CHEM', 'CHINA', 'CMW', 'CIVE',
			'CLAS', 'CO', 'COMM', 'CS', 'COOP', 'CROAT', 'DAC', 'DRAMA', 'DUTCH', 'EARTH', 'EASIA', 'ECON', 'ECE', 'ENGL', 'ESL', 'EFAS', 'ENBUS', 'ERS', 
			'ENVE', 'ENVS', 'FINE', 'FR', 'GENE', 'GEOG', 'GEOE', 'GER', 'GERON', 'GBDA', 'GRK', 'HLTH', 'HIST', 'HRM', 'HUMSC', 'IS', 'INDEV', 'INTST', 
			'INTTS', 'ITAL', 'ITALST', 'JAPAN', 'JS', 'KIN', 'INTEG', 'KOREA', 'LAT', 'LS', 'MATBUS', 'MSCI', 'MNS', 'MATH', 'MTHEL', 'ME', 'MTE', 'MEDVL',
			'MUSIC', 'NE', 'NATST', 'OPTOM', 'PACS', 'PHARM', 'PHIL', 'PHYS', 'PLAN', 'POLSH', 'PSCI', 'PORT', 'PD', 'PDPHRM', 'PSYCH', 'PMATH', 'REC', 'RS',
			'RUSS', 'REES', 'SCI', 'SCBUS', 'SMF', 'SDS', 'SOCWK', 'SWREN', 'STV', 'SOC', 'SE', 'SPAN', 'SPCOM', 'STAT', 'SI', 'SYDE', 'UNIT', 'VCULT', 'WS',
			'WKRPT']
alldays = ['Th', 'Su', 'M', 'T', 'W', 'F', 'S']
allbuildings = ['AAR', 'ACW', 'AL', 'ARC', 'B1', 'B2', 'BAU', 'BMH', 'BRH', 'C2', 'CGR', 'CIF', 'CLN', 'CLV', 'COG', 'COM', 'CPH', 'CSB', 'DC', 'DWE', 'E2',
				'E3', 'E5', 'E6', 'ECH', 'EIT', 'ERC', 'EV1', 'EV2', 'EV3', 'ESC', 'FED', 'GA', 'GH', 'GSC', 'HH', 'HMN', 'HS', 'HSC', 'IHB', 'KDC', 'LHI', 
				'LIB', 'M3', 'MC', 'MHR', 'MKV', 'ML', 'NH', 'OPT', 'PAC', 'PAS', 'PHR', 'PHY', 'QNC', 'RA2', 'RAC', 'RCH', 'REN', 'REV', 'SCH', 'SLC',
				'STJ', 'STP', 'TC', 'TH', 'UAE', 'UC', 'UWP', 'V1', 'WSS']


F = open('rooms-times.txt', 'w')

for sub in allsubs:
	term = "1139"
	#sub = "PHYS"
	num = ""

	data = {"sess" : term, "subject" : sub, "cournum" : num}
	encoded_data = urllib.urlencode(data)
	content = urllib2.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl",	encoded_data)
	soup = BeautifulSoup(content.read())
	stuff = soup.find_all("td", align="center")
	l = [str(i.text).strip() for i in stuff]
	"""
	For the record,
	0 = Subject (such as PHYS)
	1 = Subject Code (such as 121)
	2 = Units
	3 = Course Name (such as Mechanics)
	"""


	classnum, numindex = [], []
	for i in xrange(0, len(l)):
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
	for i in range(0,len(numindex)):
		#splits the class sections
		try:
			n1 = numindex[i]
			n2 = numindex[i+1]
			classes.append(l[n1:n2])
		except:
			n = numindex[i]
			classes.append(l[n:])

	timesrooms = []
	for c in classes:
		temp = []
		for i in c:
			try:
				float(i)
			except:
				if ':' in i:
					temp.append(i)
				elif any(b in i.split() for b in allbuildings):
					temp.append(' '.join(i.split()))

		timesrooms.append(temp)

	timesrooms = [i[::-1] for i in timesrooms if len(i) == 2]
	for l in timesrooms: 
		#print '  -  '.join(l)
		F.write('  -  '.join(l) + "\n")

