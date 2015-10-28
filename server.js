var express = require('express'),
    app = express(),
    path = require('path'),
    bodyParser = require('body-parser'),
    pg         = require('pg'),
    secrets    = require('./secrets');

var client = new pg.Client(secrets.conString);
client.connect();

app.use(bodyParser.urlencoded());
app.use(express.static(path.join(__dirname, 'public')));
roomsurferRouter = express.Router({mergeParams: true});
app.use('/roomsurfer', roomsurferRouter);

roomsurferRouter.route('/')
    .get(function(req, res) {
        res.sendfile('public/roomsurfer.html');
    });

roomsurferRouter.route("/api/usedrooms")
    .get(function(req, res) {
        client.query(
            "SELECT DISTINCT building, room FROM FreeRooms ORDER BY building, room",
            function(err, result) { 
                res.json(result.rows);
            }
        );
    });

roomsurferRouter.route("/api/usedrooms/:building")
    .get(function(req, res) {
        var building = req.params.building.toUpperCase();
        client.query(
            "SELECT DISTINCT room FROM FreeRooms WHERE building = ($1) ORDER BY room",
            [building], function(err, result) {
                res.json(result.rows);
            }
        );
    });

roomsurferRouter.route('/api/room/:building/')
    .get(function(req, res) {
        var building = req.params.building.toUpperCase();
        client.query(
            "SELECT room, day, starttime, endtime FROM FreeRooms WHERE building = ($1) ORDER BY room",
            [building], function(err, result) {
                res.json(result.rows);
            }
        );
    });

roomsurferRouter.route('/api/room/:building/:room')
    .get(function(req, res) {
        var building = req.params.building.toUpperCase(),
            room     = req.params.room;
        client.query(
            "SELECT day, starttime, endtime FROM FreeRooms WHERE building = ($1) and room = ($2)",
            [building, room], function(err, result) {
                res.json(result.rows);
            }
        );
    });

roomsurferRouter.route('/api/time/:day/:start?/:end?')
    .get(function(req, res) {
        var day   = req.params.day,
            start = parseInt(req.params.start),
            end   = parseInt(req.params.end);

        day = day.charAt(0).toUpperCase() + day.slice(1);

        if (!start) {
            start = 0;
        }
        if (!end) {
            end = 1439;
        }

        client.query(
            "SELECT building, room FROM FreeRooms WHERE day = ($1) and starttime <= ($2) and endtime >= ($3)",
            [day, start, end], function(err, result) {
                res.json(result.rows);
            }
        );
    });

app.listen(4000);
console.log('Roomsurfer started on 4000...');

module.exports = app;
