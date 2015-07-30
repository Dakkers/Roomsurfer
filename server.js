var express = require('express'),
    app = express(),
    path = require('path'),
    bodyParser = require('body-parser'),
    pg         = require('pg'),
    secrets    = require('./secrets');

var conString = secrets.conString;
var client = new pg.Client(conString);
client.connect()

// var conn = mysql.createConnection({
//     host     : secrets.sqlHost,
//     user     : secrets.sqlUser,
//     password : secrets.sqlPassword,
//     database : "Roomsurfer"
// });

// conn.connect();


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
        client.query(
            "SELECT DISTINCT room FROM FreeRooms WHERE building = ($1) ORDER BY room",
            [building], function(err, result) {
                res.json(result.rows);
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
        client.query(
            "SELECT room, day, starttime, endtime FROM FreeRooms WHERE building = ($1) ORDER BY room",
            [building], function(err, result) {
                if (result.rows.length === 0)
                    res.json({"invalid": 1})
                else
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
                if (result.rows.length === 0)
                    res.json({"invalid": 1})
                else
                    res.json(result.rows);
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

        client.query(
            "SELECT building, room FROM FreeRooms WHERE day = ($1) and starttime <= ($2) and endtime >= ($3)",
            [day, start, end], function(err, result) {
                console.log(day, start, end);
                res.json(result.rows);
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