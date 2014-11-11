App.Router.map(function() {
	this.resource('rooms');
	this.resource('times');
});

App.ApplicationRoute = Ember.Route.extend({
	model: function() {
		// $.getJSON('/roomsurfer/api/usedrooms').then(function(data) {

		// })
	}
});

App.RoomsRoute = Ember.Route.extend({
	model: function() {
		return;
	}
});

App.TimesRoute = Ember.Route.extend({
	model: function() {
		return;
	}
});