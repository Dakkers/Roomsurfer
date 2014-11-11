Roomsurfer
==========

Roomsurfer is a web application that allows University of Waterloo students to find rooms on campus to study in. The user can check what time a room is available at, or they can find all rooms that are available during a certain time interval. there is also an API available (currently in the works).

### API Usage
the Roomsurfer API is very simple - you can only send GET requests using a URL. all queries must be sent to ```http://stdako.com/roomsurfer/api/METHOD```, where METHOD is replaced by one of the methods described below.

#### usedrooms
find all of the rooms (building name and room number) that are being used this term. returns array of objects. example output:
```javascript
[
	{"building": "CPH", "rooms": ["1346", "3607", "3623", "	3679", "4333"]},
	{"building": "PAS", "rooms": ["1229", "2083", "2086"]},
	...
]
```

#### usedrooms/:building
find all of the room numbers being used in a specific building this term. ```:building``` must be the building code returns an object. example output (http://stdako.com/roomsurfer/api/usedrooms/PHY) :

```javascript
{"building": "PHY", "rooms": ["145","150","235","313"]}
```

#### room/:room
find all of the times that a room is free. returns an object. ```:room``` must be of the form BUILDINGCODE-ROOMNUM (e.g. RCH-308, mc-4045 ; both styles work). example output (http://stdako.com/roomsurfer/api/room/PHY-145):
```javascript
{"room": "PHY 145", 
 "times": {
 	"Th": [[690,860],[930,1310]],
 	"M":[[510,620],[750,800],[870,1310]],
 	"T":[[690,1310]],
 	"W":[[510,620],[750,800],[870,1310]],
 	"F":[[510,560],[750,800],[930,1310]]
 }
}
```

all times are in minutes - use your own function to convert at the moment (formatting options will be available in the near future).

#### time/:time
find all of the rooms that are free at a specific time. returns an object. ```:time``` must be of the form START-END-DAY (e.g. 780-1130-M). human-readable times are not supported yet. example output ():
```javascript
{"time": "510,860,M",
 "rooms": ["AL 105","AL 124","AL 209","ARC 1001","ARC 1101","ARC 2026","ARC 3103","B1 370","B2 350","BMH 1016","CGR 1111","CGR 1300","CPH 1346","CPH 4333","DWE 1515","DWE 2529","DWE 3517","DWE 3522","E2 1303","E2 1303A","E5 6004","E6 2024","E6 4022","ECH 1205","EIT 1015","EIT 3141","EV3 3408","HH 124","HH 138","HH 280","HH 336","MC 1085","ML 117","OPT 309","PAS 2083","PAS 2086","PHR 1006","QNC 1502","QNC 1507","QNC 2502","RCH 204","RCH 302","REN 0104","REN 0106","REN 0203","REN 0402","REN 2102","REN 2104","REN 2107","STJ 1036","STJ 3014","STJ 3027","STP 201"]
}
```


### Version History
#### 1.0.0 (current)
- switched to using a MEEN stack (MongoDB/Express/Ember/Node)
- created the api
- in process of fixing [#4](https://github.com/StDako/Roomsurfer/issues/4)

#### 0.3.14
- switched from using jQuery for "data-binding" to KnockoutJS

#### 0.2.71
- created Mongo database on my DigitalOcean server (i.e. created a backend)

#### 0.1.61
- original app
- loaded ALL of the data into the user's browser and called it through there (I did not own a server or know anything about web-dev / back-end stuff, so yeah)
