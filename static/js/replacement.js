function converttoclock(m) {
	// given an integer number of minutes, converts to 12-hour clock
	var when;
	if (m >= 780) {
		// 780 mins = 13 hours = 1 PM
		when = 'PM';
		m = m - 12*60;
	} else if (m >= 720 && m < 780) {
		when = 'PM';
	} else {
		when = 'AM';
	}

	var hour = Math.floor(m/60).toString(),
		min = (m%60).toString();

	if (parseInt(hour) < 10)
		hour = '0' + hour;

	if (parseInt(min) < 10)
		min = '0' + min;

	return hour + ':' + min + ' ' + when;
}

function converttoint(time) {
	// given a clock time (string), converts to minutes
	time = time.split(':');
	var hour = parseInt(time[0],10),
		min = parseInt(time[1].substring(0,2),10),
		period = time[1].substring(3,5);

	if ((period === 'PM') && (hour !== 12))
		hour += 12;

	return 60*hour + min;
}

function convToTimes(L) {
	//given an array of arrays (of two ints (start/endtimes))
	//returns the time interval in a 12-hour clock format for each array
	L_return = new Array(L.length);
	for (var i=0; i < L.length; i++) {
		var l = L[i],
			st = converttoclock(l[0]), 
			et = converttoclock(l[1]),
			interval = st + ' - ' + et;

		L_return[i] = interval;
	}
	return L_return;
}

function dayname(abbrv) {
	var hmph = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'Th': 'Thursday', 'F': 'Friday'};
	return hmph[abbrv];
}

function sortNum(a,b) {
	return a - b;
}


$(document).ready(function () {
	var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
		allCodes = {}; //format: {"PHY": ["145", "150", ...], ...}
	$("#header").hide().fadeIn(600);
	$("#splash").hide().fadeIn(800);

	function AppViewModel() {
		self = this;

		// ROOM STUFF
		// list of building names & roomnumbers
		self.codes = ko.observableArray();
		self.rooms = ko.observableArray();
		// current selected building & roomnumber
		self.building = ko.observable("");
		self.roomnum = ko.observable("");
		self.roomInfo = ko.computed(function() {
			return self.building() + " " + self.roomnum();
		},self);
		
		// when the user changes building, update list of roomnumbers (i.e. combobox)
		self.building.subscribe(function(b) {
			var newRooms = allCodes[b];
			if (typeof newRooms !== 'undefined')
				self.rooms(newRooms);
		}, self);

		// the free times for each day
		self.roomFreeTimes = ko.observableArray([{dayName: 'Monday', dayTimes: ko.observableArray()}, {dayName: 'Tuesday', dayTimes: ko.observableArray()},{dayName: 'Wednesday', dayTimes: ko.observableArray()},{dayName: 'Thursday', dayTimes: ko.observableArray()},{dayName: 'Friday', dayTimes: ko.observableArray()}]);

		self.getTimes = function() {
			$.ajax({
				url: 'http://127.0.0.1:5000/roomsurferKO',
				type: 'POST',
				data: {'type': 'ROOM', 'room': self.roomInfo()}
			}).success(function(data) {
				data = JSON.parse(data);
				self.roomFreeTimes()[0]['dayTimes'](convToTimes(data['M'])); self.roomFreeTimes()[1]['dayTimes'](convToTimes(data['T'])); self.roomFreeTimes()[2]['dayTimes'](convToTimes(data['W'])); self.roomFreeTimes()[3]['dayTimes'](convToTimes(data['Th'])); self.roomFreeTimes()[4]['dayTimes'](convToTimes(data['F']));
			});
		}

		// TIME STUFF
		// this makes me laugh, probably because it's 5 AM right now - no I didn't hard code this, I used Python :)
		self.allStartTimes = [{"timeVal": "8:30 AM", "intVal": "510"},{"timeVal": "9:00 AM", "intVal": "540"},{"timeVal": "9:30 AM", "intVal": "570"},{"timeVal": "10:00 AM", "intVal": "600"},		{"timeVal": "10:30 AM", "intVal": "630"},{"timeVal": "11:00 AM", "intVal": "660"},{"timeVal": "11:30 AM", "intVal": "690"},{"timeVal": "12:00 PM", "intVal": "720"},		{"timeVal": "12:30 PM", "intVal": "750"},{"timeVal": "1:00 PM", "intVal": "780"},{"timeVal": "1:30 PM", "intVal": "810"},{"timeVal": "2:00 PM", "intVal": "840"},		{"timeVal": "2:30 PM", "intVal": "870"},{"timeVal": "3:00 PM", "intVal": "900"},{"timeVal": "3:30 PM", "intVal": "930"},{"timeVal": "4:00 PM", "intVal": "960"},		{"timeVal": "4:30 PM", "intVal": "990"},{"timeVal": "5:00 PM", "intVal": "1020"},{"timeVal": "5:30 PM", "intVal": "1050"},{"timeVal": "6:00 PM", "intVal": "1080"},		{"timeVal": "6:30 PM", "intVal": "1110"},{"timeVal": "7:00 PM", "intVal": "1140"}];
		self.allEndTimes = [{"timeVal": "9:20 AM", "intVal": "560"},{"timeVal": "9:50 AM", "intVal": "590"},{"timeVal": "10:20 AM", "intVal": "620"},{"timeVal": "10:50 AM", "intVal": "650"},{"timeVal": "11:20 AM", "intVal": "680"},{"timeVal": "11:50 AM", "intVal": "710"},{"timeVal": "12:20 PM", "intVal": "740"},{"timeVal": "12:50 PM", "intVal": "770"},{"timeVal": "1:20 PM", "intVal": "800"},{"timeVal": "1:50 PM", "intVal": "830"},{"timeVal": "2:20 PM", "intVal": "860"},{"timeVal": "2:50 PM", "intVal": "890"},{"timeVal": "3:20 PM", "intVal": "920"},{"timeVal": "3:50 PM", "intVal": "950"},{"timeVal": "4:20 PM", "intVal": "980"},{"timeVal": "4:50 PM", "intVal": "1010"},{"timeVal": "5:20 PM", "intVal": "1040"},{"timeVal": "5:50 PM", "intVal": "1070"},{"timeVal": "6:20 PM", "intVal": "1100"},{"timeVal": "6:50 PM", "intVal": "1130"},{"timeVal": "7:20 PM", "intVal": "1160"},{"timeVal": "7:50 PM", "intVal": "1190"},{"timeVal": "8:20 PM", "intVal": "1220"},{"timeVal": "8:50 PM", "intVal": "1250"},{"timeVal": "9:20 PM", "intVal": "1280"},{"timeVal": "9:50 PM", "intVal": "1310"},{"timeVal": "", "intVal": ""}];
		self.allDays = ['M', 'T', 'W', 'Th', 'F'];
		self.allFreeRooms = ko.observableArray([{building: '(Hit the button to check!)', times: []}]);
		self.buttonPressedOnce = ko.observable(false);

		self.startTime = ko.observable("8:30 AM");
		self.endTime = ko.observable("9:20 AM");
		self.day = ko.observable("M");
		self.daySpan = ko.observable("Monday"); //TODO: fix this fucking variable name, lolgg 6:14 AM fffffffffffffffff

		self.timeInfo = ko.computed(function() {
			return [converttoint(self.startTime()).toString(), converttoint(self.endTime()).toString(), self.day()].join(',');
		}, this);

		// change startTime on select change
		self.changeStart = function(data, event) {
			var val = event.target.value;
			self.startTime(converttoclock(val));
		}
		// change endTime on select change
		self.changeEnd = function() {
			var val = event.target.value;
			self.endTime(converttoclock(val));
		}
		// aaaaand change the day on select change.
		self.day.subscribe(function(d) {
			self.daySpan(dayname(d));
		}, this);

		self.getRooms = function() {
			self.buttonPressedOnce(true);
			self.allFreeRooms.removeAll();

			$.ajax({
				url: 'http://127.0.0.1:5000/roomsurferKO',
				type: 'POST',
				data: {'type': 'TIME', 'time': self.timeInfo()}
			}).success(function(data) {
				console.log(data);
				data = JSON.parse(data);

				if (Object.keys(data).length === 0) {
					self.allFreeRooms.push({building: 'Sorry!', times: ['There are no rooms available at that time.']});
				} else {
					for (var key in data)
						self.allFreeRooms.push({building: key, times: data[key]});
				}
			});
		}
	}

	var AVM = new AppViewModel();

	// get all of the buildings & rooms used this term
	$.ajax({
		url: 'http://127.0.0.1:5000/roomsurferKO',
		type: 'POST',
		data: {'type': 'BUILDING'}
	}).success(function(data) {
		allCodes = JSON.parse(data);
		for (var key in allCodes)
			allCodes[key] = allCodes[key].sort(sortNum);
		var codes = Object.keys(allCodes).sort();
		var rooms = allCodes[codes[0]];
		// update the building & room selects
		AVM.codes(codes);
		AVM.rooms(rooms);
	});


	$("#splashtimes").click(function() {
		$("#splash").fadeOut(500, function() {
			$("#times-to-rooms").fadeIn(500);
			$("#times").fadeIn(500);
		});
	});

	$("#splashrooms").click(function() {
		$("#splash").fadeOut(500, function() {
			$("#rooms").fadeIn(500);
			$("#rooms-to-times").fadeIn(500);
		});
	});

	$("#rooms-to-times").click(function() {
		$("#rooms").fadeOut(500);
		$("#rooms-to-times").fadeOut(500, function() {
			$("#times").fadeIn(500);
			$("#times-to-rooms").fadeIn(500);
		});
	});

	$("#times-to-rooms").click(function() {
		$("#times").fadeOut(500);
		$("#times-to-rooms").fadeOut(500, function() {
			$("#rooms").fadeIn(500);
			$("#rooms-to-times").fadeIn(500);
		});
	});

	ko.applyBindings(AVM);
});