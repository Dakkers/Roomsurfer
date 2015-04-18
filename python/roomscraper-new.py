import urllib, urllib2
from bs4 import BeautifulSoup

# get API key
SECRETS = open('secrets.txt')
key = SECRETS.readlines()[0]
SECRETS.close()

def get_classes(sub, F):
    
    data = {"sess": "1155", "subject": sub, "cournum": ""}
    data_encoded = urllib.urlencode(data)
    content = urllib2.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl", data_encoded)
    soup = BeautifulSoup(content.read())
    table = soup.find('table')
    if table is None:
        return

    rows = table.find_all('tr', recursive=False)
    # print rows
    for i in xrange(len(rows)):
        row = rows[i]
        cells = row.find_all('td')
        if len(cells) > 1 and sub in cells[0].text:
            num = cells[1].text
            print sub, num
            F.write('%s %s\n' % (sub, num))


# get subjects
scus = urllib2.urlopen('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')
soup_subs = BeautifulSoup(scus.read())

subs = soup_subs.find_all('select')[1].find_all('option')
subs = [sub.text.strip() for sub in subs]
subs_to_ignore = ['ARCH', 'PD', 'PDARCH', 'PDPHRM', 'WHMIS', 'COOP', 'INTERN', 'BASE', 'ELPE', 'WKRPT']

F_CLASSES = open('./classes.txt', 'w')
for sub in subs:
    if sub not in subs_to_ignore:
        get_classes(sub, F_CLASSES)

# result = urllib2.urlopen('https://api.uwaterloo.ca/v2/courses/PHYS/112/schedule.json?key=3528052876f446032fde35b4a751ec5c')
# print result.read()

F_CLASSES.close()
