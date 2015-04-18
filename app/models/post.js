var mongoose = require('mongoose');

var postSchema = mongoose.Schema({
	title: String,
	content: Array,
	topics: Array,
	date: String,
	number: Number
});

module.exports = mongoose.model("blog_posts", postSchema);