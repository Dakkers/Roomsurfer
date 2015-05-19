import urllib
import urllib2
import json
from bs4 import BeautifulSoup

# get API key
SECRETS = open('secrets.txt')
key = SECRETS.readlines()[0]
SECRETS.close()


# THIS IS PROBABLY NOT NEEDED
def get_classes(sub):
    """
    Given a subject name, writes all of the courses offered in that subject for
    the term to a file.

    Parameters
    ----------
    sub : string
        A subject, like PHYS or AMATH.

    Returns
    -------
    classes : list
        A list of strings representing the class numbers. (Strings are used
        because some class numbers have letters in them too...)
    """
    classes = []

    # get the webpage...
    data = {"sess": "1155", "subject": sub, "cournum": ""}
    data_encoded = urllib.urlencode(data)
    content = urllib2.urlopen("http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl", data_encoded)
    soup = BeautifulSoup(content.read())
    table = soup.find('table')

    if table is not None:
        # loop through each block of information
        rows = table.find_all('tr', recursive=False)
        for i in xrange(len(rows)):
            row = rows[i]
            cells = row.find_all('td')
            if len(cells) > 1 and sub in cells[0].text:
                num = cells[1].text

                # ignore labs...
                if num[-1] == 'L':
                    continue

                classes.append(num)

    return classes


def get_subjects():
    """
    Creates a list of subjects, ignoring some we don't care about.

    Returns
    -------
    list
        List of subjects in alphabetical order, e.g. ['AMATH', 'CS', ...]. All
        elements are strings.
    """
    subs_to_keep = []

    scus = urllib2.urlopen('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')
    soup_subs = BeautifulSoup(scus.read())

    # get all of the subject codes (AMATH, CS, ...) by scraping
    subs = soup_subs.find_all('select')[1].find_all('option')
    subs = [sub.text.strip() for sub in subs]
    subs_to_ignore = ['ARCH', 'PD', 'PDARCH', 'PDPHRM', 'WHMIS', 'COOP', 'INTERN', 'BASE', 'ELPE', 'WKRPT']

    for sub in subs:
        if sub not in subs_to_ignore:
            subs_to_keep.append(sub)

    return subs_to_keep


def get_times(d):
    # d is currently a dictionary, but it will later just be the course
    # sub/num
    raw_data = {}

    for section in d['data']:
        for c in section['classes']:
            is_cancelled = c['date']['is_cancelled']
            is_tba       = c['date']['is_tba']

            # ignore classes that were cancelled, or are TBA
            if not is_cancelled and not is_tba:
                building = c['location']['building']
                room = c['location']['room']

                # ignore classes that don't have an assigned building/room
                if building is not None and room is not None:
                    start = convert_clock_to_minutes(c['date']['start_time'])
                    end   = convert_clock_to_minutes(c['date']['end_time'])
                    days  = get_days(c['date']['weekdays'])
                    time  = [start, end]
                    for day in days:
                        add_time(raw_data, building, room, day, time)

    return raw_data


def sort_and_merge_times(data):
    for building in data:
        for room in data[building]:
            for day in data[building][room]:
                data[building][room][day].sort(cmp=lambda t1, t2: t1[0]-t2[0])
                merge_times(data[building][room][day])
    return data


def merge_times(times):
    # act on the list itself
    i, N = 0, len(times) - 1
    while i < N:
        start_curr, end_curr = times[i]
        start_next, end_next = times[i+1]
        if start_next - 10 <= end_curr:
            times[i][1] = end_next
            times.pop(i+1)
            N -= 1
        else:
            i += 1


def get_days(s):
    """
    Given a string of days (M, T, W, Th, F), e.g. 'MTTh', a list is created
    with the days separated, e.g. ['M', 'T', 'Th']

    Parameters
    ----------
    s : string
        A string of days in abbreviated form: M is Monday, T is Tuesday, W is
        Wednesday, Th is Thursday, F is Friday.

    Returns
    -------
    list
        A list of days in abbreviated form; not necessarily in order.
    """
    days = []

    # remove 'Th' from s, as then the rest of the characters in the string are
    # the days (the 'h' makes things a bit complicated...)
    if 'Th' in s:
        days.append('Th')
        s = s.replace('Th', '')

    return days + [day for day in s]


def convert_clock_to_minutes(clock_time):
    """
    Converts 24-hour clock time to minutes.

    Parameters
    ----------
    clock_time : str
        24-hour clock time, colon-delimited, e.g. 14:30.

    Returns
    -------
    int
        Number of minutes equivalent to the clock time.
    """
    hour, minute = [int(i) for i in clock_time.split(':')]
    return 60*hour + minute


def add_time(d, building, room, day, time):
    if building not in d:
        d[building] = {}
    if room not in d[building]:
        d[building][room] = {}
    if day not in d[building][room]:
        d[building][room][day] = []
    if time not in d[building][room][day]:
        d[building][room][day].append(time)


# temporary
example = open('./example.json')
data = json.loads(example.read())

print sort_and_merge_times(get_times(data))


# result = urllib2.urlopen('https://api.uwaterloo.ca/v2/terms/1155/MATH/schedule.json?key=%s' % key)
# print result.read()
