var app = require('./../server'),
  async   = require('async'),
  pg      = require('pg'),
  request = require('supertest'),
  should  = require('should'),
  secrets = require('./../secrets');

describe('testing the API', function() {

  var insertData = function(client, queryString, arr, cb) {
    client.query(queryString, function(err, result) {
      // console.log(result.rows);
      arr.length = result.rows.length;
      for (var i=0; i<arr.length; i++) {
        arr[i] = result.rows[i];
      }
      cb();
    });
  };

  // good variable names are for suckers
  var usedrooms = new Array(), usedroomsPHY = new Array(), usedroomsFake = new Array(),
    roomPHY = new Array(), roomPHY145 = new Array(), timeM = new Array(), timeM740 = new Array(),
    timeM740810 = new Array(),

    usedroomsQ = "SELECT DISTINCT building, room FROM FreeRooms ORDER BY building, room",
    usedroomsPHYQ = "SELECT DISTINCT room FROM FreeRooms WHERE building = 'PHY' ORDER BY room",
    usedroomsFakeQ = "SELECT DISTINCT room FROM FreeRooms WHERE building = 'FAKE' ORDER BY room",
    roomPHYQ = "SELECT room, day, starttime, endtime FROM FreeRooms WHERE building = 'PHY' ORDER BY room",
    roomPHY145Q = "SELECT day, starttime, endtime FROM FreeRooms WHERE building = 'PHY' and room = '145'",
    timeMQ = "SELECT building, room FROM FreeRooms WHERE day = 'M' and starttime <= 0 and endtime >= 1439",
    timeM740Q = "SELECT building, room FROM FreeRooms WHERE day = 'M' and starttime <= 740 and endtime >= 1439",
    timeM740810Q = "SELECT building, room FROM FreeRooms WHERE day = 'M' and starttime <= 740 and endtime >= 810";

  before('get the queries from the DB', function(done) {
    var client = new pg.Client(secrets.conString);
    client.connect();

    async.series([
      function(cb) { insertData(client, usedroomsQ, usedrooms, cb); },
      function(cb) { insertData(client, usedroomsPHYQ, usedroomsPHY, cb); },
      function(cb) { insertData(client, usedroomsFakeQ, usedroomsFake, cb); },
      function(cb) { insertData(client, roomPHYQ, roomPHY, cb); },
      function(cb) { insertData(client, roomPHY145Q, roomPHY145, cb); },
      function(cb) { insertData(client, timeMQ, timeM, cb); },
      function(cb) { insertData(client, timeM740Q, timeM740, cb); },
      function(cb) { insertData(client, timeM740810Q, timeM740810, cb); },
    ], done);
  });

  var tests = [
    { expected: usedrooms, query: 'usedrooms' },
    { expected: usedroomsPHY, query: 'usedrooms/PHY' },
    { expected: usedroomsFake, query: 'usedrooms/FAKE' },
    { expected: roomPHY, query: 'room/PHY' },
    { expected: roomPHY145, query: 'room/PHY/145' },
    { expected: timeM, query: 'time/M' },
    { expected: timeM740, query: 'time/M/740' },
    { expected: timeM740810, query: 'time/M/740/810' },
  ];

  tests.forEach(function(test) {
    it('should query /' + test.query, function(done) {
      request(app)
        .get('/roomsurfer/api/' + test.query)
        .expect('rest-type', 'json')
        .end(function(err, res) {
          test.expected.should.eql(res.body);
          done();
        });
    });
  });
});
