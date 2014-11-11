var mongoose = require('mongoose');

var postSchema = mongoose.Schema({
	title: String,
	content: String,
	topics: Array,
	date: String,
	number: String
});

module.exports = mongoose.model("blog_posts", postSchema);