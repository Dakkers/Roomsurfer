var mongoose = require('mongoose');

timeSchema = mongoose.Schema({
	time: String,
	rooms: Array
});

module.exports = mongoose.model("roomsurfer_rooms", timeSchema);