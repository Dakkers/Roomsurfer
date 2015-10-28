# Roomsurfer

Roomsurfer is a web application that allows University of Waterloo students to find rooms on campus to study in. The user can check what time a room is available at, or they can find all rooms that are available during a certain time interval. there is also an API available (currently in the works).

## API Usage
The Roomsurfer API is very simple - you can only send GET requests using a URL. All queries must be sent to `http://saintdako.com/roomsurfer/api/METHOD`, where METHOD is replaced by one of the methods described below.

### `usedrooms`
Find all of the rooms (building name and room number) that are being used this term. Returns an array of objects, where each object is of the form `{"building": BUILDING, "room": NUMBER}`.

Example output:

```javascript
[
    {"building": "AL", "room": "105"}, {"building": "AL", "room": "113"}, ...
    {"building": "B1", "room": "169"}, {"building": "B1", "room": "266"}, ...
    ...
]
```

### `usedrooms/:building`
Find all of the room numbers being used in a specific building this term. `building` is the building code. Returns an array of objects, where each object is of the form `{"room": NUMBER}`.

Example output (http://saintdako.com/roomsurfer/api/usedrooms/EIT) :

```javascript
[
    {"room":"1009"}, {"room":"1013"}, {"room":"1015"}, {"room":"2053"}, {"room":"3141"}, {"room":"3145"}, {"room":"3151"}
]
```

### `room/:building`
Find all of the times that all of the rooms in a specified building are free. `building` is the building code. Returns an array of objects, where each object is of the form `{"room": ROOM, "day": DAY, "starttime": STARTTIME, "endtime": ENDTIME}`, where:

- `ROOM` is a room number (integer)
- `DAY` is one of: `M`, `T`, `W`, `Th`, `F` (string)
- `STARTTIME` is the number of minutes (integer) where the room's free period begins, e.g. 510 represents 8:30 AM
- `ENDTIME` is the number of minutes (integer) where the room's free period ends

Example output (http://saintdako.com/roomsurfer/api/room/PHY):

```javascript
[
    {"room":"145","day":"M","starttime":0,"endtime":510},   {"room":"145","day":"F","starttime":1010,"endtime":1439}, ...
    {"room":"150","day":"F","starttime":680,"endtime":870}, {"room":"150","day":"F","starttime":920,"endtime":1439}, ...
    ...
```

### room/:building/:room
Find all of the times that a specified room in a specified building is free.  `building` is the building code, `room` is the room number. Returns an array of objects, where each object is of the form `{"day": DAY, "starttime": STARTTIME, "endtime": ENDTIME}`.

Example output (http://saintdako.com/roomsurfer/api/room/PHY/145):

```javascript
[
    {"day":"M","starttime":0,"endtime":510},
    {"day":"M","starttime":1100,"endtime":1439},
    {"day":"T","starttime":0,"endtime":510},
    ...
]
```

### time/:day/:start?/:end?
Find all of the rooms that are free at a specific time. `day` is one of `M`, `T`, `W`, `Th`, `F`, `start` is the room's free period start time in minutes, and `end` is the end time. If `start` is not specified, it defaults to `0`. If `end` is not specified, it defaults to `1439` (11:59 PM). Returns an array of objects, where each object is of the form: `{"building": BUILDING, "room": NUMBER}`.

Example output (http://saintdako.com/roomsurfer/api/time/M):

```javascript
[
    {"building":"CPH","room":"3602"},{"building":"CPH","room":"3607"}, ...
    {"building":"PAS","room":"1241"},{"building":"PAS","room":"2438"}, ...
    ...
```

## Getting the Data Yourself
If you want to store the data on your own machine instead of using the API, use the `python/roomscraper.py` script. Make sure to create a database called `Roomsurfer`.

Inside this directory, create a `secrets.txt` file with the following content:

```
YOUR_UW_API_KEY
YOUR_POSTGRES_USERNAME
YOUR_POSTGRES_PASSWORD
```

If you want to store the raw JSON data, uncomment `store_raw_data(TERM, key)`. Then you can run the script, specifying the term number using  the `TERM` variable. If you did not uncomment `store_raw_data`, then you will have to change

```
used = get_times(TERM, key, local_data=True)
```

to

```
used = get_times(TERM, key, local_data=False)
```

The table name is `FreeRooms` and you can check `server.js` for how to query it.

## Version History
### 1.3.0
- added tests for validating API response data
- `server.js` now exports the Express application (used in tests)

### 1.2.1
- fixed a bug that prevented Thursday times from appearing

### 1.2.0
- switched to PostgreSQL
- fixed front-end

### 1.1.0
- switched to MySQL

### 1.0.0
- switched to using a MEAN stack (MongoDB/Express/Angular/Node)
- created the api
- in process of fixing [#4](https://github.com/StDako/Roomsurfer/issues/4)

### 0.3.14
- switched from using jQuery for "data-binding" to KnockoutJS

### 0.2.71
- created Mongo database on my DigitalOcean server (i.e. created a backend)

### 0.1.61
- original app
- loaded ALL of the data into the user's browser and called it through there (I did not own a server or know anything about web-dev / back-end stuff, so yeah)
