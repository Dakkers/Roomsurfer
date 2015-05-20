import urllib
import urllib2
import json
import os
import MySQLdb
from bs4 import BeautifulSoup


# get API key
SECRETS = open('secrets.txt')
key  = SECRETS.readline().strip()
user = SECRETS.readline().strip()
pw   = SECRETS.readline().strip()
SECRETS.close()

# SQL setup
CONNECTED = False
try:
    roomsurfer = MySQLdb.connect(host="localhost", user=user, passwd=pw, db="Roomsurfer")
    cur = roomsurfer.cursor()
    CONNECTED = True
except:
    print 'Failed to connect to database "Roomsurfer".'

# the current term number
TERM = 1155


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


def get_times(d, raw_data, subject):
    """
    Given a dict of already-existing (or empty) data and a subject, the
    uWaterloo API is used to get all of the classes offered in the current
    term. Then, the classes are iterated over, getting the building name and
    room number, and adding the time that the space is used at to the data.

    Mutates an existing data set.

    Parameters
    ----------
    raw_data : dict
        Data already collected thus far, or empty. Formatted like so:
            
            {'PHY':
                '145': {
                    'M': [[510,570], [690,740]]
                }
            }

        i.e. BUILDING -> ROOM -> DAY -> LIST OF TIMES
    subject : str
        The subject name, in its short-form (e.g. 'PHY').
    """

    # subject_info = urllib2.urlopen(
    #                 'https://api.uwaterloo.ca/v2/terms/%s/%s/schedule.json?key=%s' % (TERM, subject, key)
    #                )
    # d = json.loads(subject_info.read())

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
    """
    Add a (free or used) time to a data set. The nested values are created as
    needed (so if a building does not yet exist in the data set, it is
    initialized, then the room, etc.).

    Mutates an existing data set.

    Parameters
    ----------
    d : dict
        The data set to add to.
    building : str
        The building's short-form code (e.g. 'PHY').
    room : str
        The room number, as a string (e.g. '145').
    day : str
        The day's short-form code (e.g. 'M').
    time : list
        The beginning and end time, as a list (e.g. [750, 800]).
    """
    if building not in d:
        d[building] = {}
    if room not in d[building]:
        d[building][room] = {}
    if day not in d[building][room]:
        d[building][room][day] = []
    if time not in d[building][room][day]:
        d[building][room][day].append(time)


def get_free_times(used_times):
    """
    Given a list of used times (pairs of start and end times), the
    corresponding free times are generated.

    Parameters
    ----------
    used_times : list
        A list of lists, where each nested list is a pair of integers that
        represent the start time and end time of when the class is used.

    Returns
    -------
    list
        A list of lists, similar to the input, but the pairs represent when the
        class is free.
    """
    free_times = []
    free_start, free_end = 0, 1439     # beginning, end of day

    for used_time in used_times:
        # 'free period' ends when the class starts
        free_end = used_time[0]
        free_times.append([free_start, free_end])

        # next 'free period' starts when the class ends
        free_start = used_time[1]

    # last class' end time to end of day
    free_times.append([free_start, 1439])

    return free_times


def get_all_free_times(used):
    """
    Given the data representing the times that rooms are booked at, the
    corresponding times that the rooms are free at is generated.

    Parameters
    ----------
    used : dict
        Data for all times that rooms are booked at.

    Returns
    -------
    dict
        Data for all times that rooms are free at.
    """
    free = {}
    days = ['M', 'T', 'W', 'Th', 'F']

    for building in used:
        for room in used[building]:
            for day in days:
                # if the room is used on this day, get its times, sort them,
                # merge them, get the corresponding free times and add them to
                # the free data
                if day in used[building][room]:
                    used[building][room][day].sort(cmp=lambda t1, t2: t1[0]-t2[0])
                    merge_times(used[building][room][day])
                    add_time(free, building, room, day,
                             get_free_times(used[building][room][day]))

                # otherwise, it's not in use on this day, i.e. it's free all
                # day; then, add it to the free data
                else:
                    # passing an empty list to get_free_times will result in
                    # a pair of times representing the entire day
                    add_time(free, building, room, day, get_free_times([]))

    return free


def store_raw_data():
    """
    All 'raw data' (i.e. UW API return data) for each subject is written to a
    file in a folder (one file per subject).
    """
    subs = get_subjects()

    if not os.path.isdir('./raw_data'):
        os.mkdir('./raw_data')

    for sub in subs:
        subject_info = urllib2.urlopen(
                        'https://api.uwaterloo.ca/v2/terms/%s/%s/schedule.json?key=%s' % (TERM, sub, key)
                       )

        f = open('./raw_data/%s.txt' % sub, 'w')
        f.write(subject_info.read())
        f.close()


def dump_to_sql(free, connected):
    if not connected:
        return

    days = ['M', 'T', 'W', 'Th', 'F']

    if cur.execute("SHOW TABLES LIKE 'FreeRooms'"):
        cur.execute("DROP TABLE FreeRooms")
    cur.execute( ("CREATE TABLE FreeRooms ("
                   "building VARCHAR(4),"
                   "room     VARCHAR(6),"
                   "day      VARCHAR(2),"
                   "start    SMALLINT,"
                   "end      SMALLINT )"
                  ) )

    for building in free:
        for room in free[building]:
            for day in days:
                times = free[building][room][day]
                print times
                for time in times[0]:
                    print time
                    cur.execute( ("INSERT INTO FreeRooms (building, room, day, start,"
                                  "end) VALUES ('%s', '%s', '%s', '%d', '%d')" % (
                                  building, room, day, time[0], time[1]) ) )

    roomsurfer.commit()


# temporary
example = open('./example.json')
data = json.loads(example.read())

used = {}
get_times(data, used, 'PHYS')

free = get_all_free_times(used)
print free
dump_to_sql(free, CONNECTED)

roomsurfer.close()

# result = urllib2.urlopen('https://api.uwaterloo.ca/v2/terms/1155/MATH/schedule.json?key=%s' % key)
# print result.read()
