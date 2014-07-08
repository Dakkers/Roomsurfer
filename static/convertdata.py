from pymongo import MongoClient
import json
client = MongoClient()
db = client.roomsurfer
fts = db.freetimes_sorted
fr = db.freerooms
# FILE = open('1141times.json')
# d = json.load(FILE)
# FILE.close()

# for room in d['freetimes_sorted']:
# 	info = d['freetimes_sorted'][room]
# 	fts.insert({'info': info, 'room': room})

# for time in d['freerooms']:
# 	info = d['freerooms'][time]
# 	fr.insert({'info': info, 'time': time})

codes = {}

for i in fts.find():

	building, num = [j.encode('ascii', 'ignore') for j in i['room'].split(' ')]
	if building in codes:
		codes[building].append(num)
	else:
		codes[building] = [num]

	# sub = i['room'].split(' ')[0].encode('ascii', 'ignore')
	# if sub not in S:
	# 	S += sub+';'

print codes.keys()