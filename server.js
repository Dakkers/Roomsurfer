var express = require('express'),
    app = express(),
    path = require('path'),
    bodyParser = require('body-parser'),
    mongoose = require('mongoose');

var Post = require('./app/models/post'),
    Room = require('./app/models/room'),
    Time = require('./app/models/time'),
    Building = require('./app/models/building');
mongoose.connect('mongodb://localhost/stdako');

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
        Building.find({})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            res.json(data);
        });
    });

roomsurferRouter.route("/api/usedrooms/:building")
    .get(function(req, res) {
        Building.findOne({building: req.params.building.toUpperCase()})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            res.json(data);
        });
    });

roomsurferRouter.route('/api/room/:room')
    .get(function(req, res) {
        Room.findOne({room: req.params.room.replace("-"," ").toUpperCase()})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            // TODO
            // if (format === true)
            //    format time from minutes to 12-hour clock.
            res.json(data);
        });
    });

roomsurferRouter.route('/api/time/:time')
    .get(function(req, res) {
        // TODO
        // if (format === true)
        //    format time from minutes to 12-hour clock
        Time.findOne({time: req.params.time.replace(/-/g,",")})
        .select({_id: 0})
        .lean()
        .exec(function(err, data) {
            console.log(req.params.time.replace(/-/g,","));
            res.json(data);
        });
    });

app.listen(4000);
console.log('Roomsurfer started on 4000...');