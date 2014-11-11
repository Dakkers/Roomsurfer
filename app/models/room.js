var mongoose = require('mongoose');

roomSchema = mongoose.Schema({
	room: String,
	times: Array
});

module.exports = mongoose.model("roomsurfer_times", roomSchema);