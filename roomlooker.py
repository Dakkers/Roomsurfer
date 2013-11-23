"""
This program, in particular, is used for room -> freetimes. Given a room,
it will post all of the freetimes.
"""
import json
FILE = open('fall2013times.txt')
loaded = json.load(FILE)
fts = loaded['freetimes_sorted']
FILE.close()

i = 'PHY 145'