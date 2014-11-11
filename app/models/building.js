var mongoose = require('mongoose');

buildingSchema = mongoose.Schema({
	building: String,
	rooms: Array
});

module.exports = mongoose.model("roomsurfer_usedrooms", buildingSchema);