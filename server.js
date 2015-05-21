var express = require('express'),
    app = express(),
    path = require('path'),
    bodyParser = require('body-parser'),
    mongoose   = require('mongoose'),
    mysql      = require('mysql'),
    secrets    = require('./secrets');

var conn = mysql.createConnection({
    host     : secrets.sqlHost,
    user     : secrets.sqlUser,
    password : secrets.sqlPassword,
    database : "Roomsurfer"
});

conn.connect();

var Room = require('./app/models/room'),
    Time = require('./app/models/time'),
    Building = require('./app/models/building');
// mongoose.connect('mongodb://localhost/stdako');

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
        conn.query(
            "SELECT DISTINCT building, room FROM FreeRooms ORDER BY building, room",
            function(err, rows) { 
                res.json(rows);
            }
        );

        /*
        Building.find({})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            res.json(data);
        });
        */
    });

roomsurferRouter.route("/api/usedrooms/:building")
    .get(function(req, res) {
        var building = req.params.building.toUpperCase();
        conn.query(
            "SELECT DISTINCT room FROM FreeRooms WHERE building = ? ORDER BY room",
            [building], function(err, rows) {
                res.json(rows);
            }
        );

        /*
        Building.findOne({building: req.params.building.toUpperCase()})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            res.json(data);
        });
        */
    });

roomsurferRouter.route('/api/room/:building/')
    .get(function(req, res) {
        var building = req.params.building.toUpperCase();
        conn.query(
            "SELECT room, day, start, end FROM FreeRooms WHERE building = ? ORDER BY room",
            [building], function(err, rows) {
                res.json(rows);
            }
        );
    });

roomsurferRouter.route('/api/room/:building/:room')
    .get(function(req, res) {
        var building = req.params.building.toUpperCase(),
            room     = req.params.room;
        conn.query(
            "SELECT day, start, end FROM FreeRooms WHERE building = ? and room = ?",
            [building, room], function(err, rows) {
                res.json(rows);
            }
        );

        /*
        Room.findOne({room: req.params.room.replace("-"," ").toUpperCase()})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            // TODO
            // if (format === true)
            //    format time from minutes to 12-hour clock.
            res.json(data);
        });
        */
    });

roomsurferRouter.route('/api/time/:day/:start?/:end?')
    .get(function(req, res) {
        // TODO
        // if (format === true)
        //    format time from minutes to 12-hour clock
        var day   = req.params.day.toUpperCase(),
            start = parseInt(req.params.start),
            end   = parseInt(req.params.end);

        if (!start)
            start = 0;
        if (!end)
            end = 1439;

        conn.query(
            "SELECT building, room FROM FreeRooms WHERE day = ? and start = ? and end = ?",
            [day, start, end], function(err, rows) {
                res.json(rows);
            }
        )
        /*
        Time.findOne({time: req.params.time.replace(/-/g,",")})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            console.log(req.params.time.replace(/-/g,","));
            res.json(data);
        });
        */
    });

app.listen(4000);
console.log('Roomsurfer started on 4000...');