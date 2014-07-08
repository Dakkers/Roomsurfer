function converttoclock(m) {
	//given a number of minutes, converts to 12-hour clock
	var when;
	if (m >= 780) {
		//780 mins = 13 hours = 1 PM
		when = 'PM';
		m = m - 12*60;
	} else if (m >= 720 && m < 780) {
		when = 'PM';
	} else {
		when = 'AM';
	}

	var hour = Math.floor(m/60).toString(),
		min = (m%60).toString();

	if (parseInt(hour) < 10) {	
		hour = '0' + hour; 	
	}
	if (parseInt(min) < 10) { 
		min = '0' + min;
	}

	return hour + ':' + min + ' ' + when;
}

function convertToTimes(L) {
	//given an array of arrays (of two ints (start/endtimes))
	//returns the time interval in a 12-hour clock format for each array
	L_return = new Array(L.length);
	for (var i=0; i < L.length; i++) {
		var l = L[i],
			st = converttoclock(l[0]), et = converttoclock(l[1]),
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
		masterdict = {},
		allCodes = {}; //format: {"PHY": ["145", "150", ...], ...}
	$("#header").hide().fadeIn(600);
	$("#splash").hide().fadeIn(800);

	// get all of the buildings and rooms used
	$.ajax({
		url: 'http://127.0.0.1:5000/roomsurfer',
		type: 'POST',
		data: JSON.stringify({'type': 'BUILDING'})
	}).success(function(data) {
		allCodes = JSON.parse(data);
		var codes = Object.keys(allCodes); // array of building codes
		codes.sort();
		var rooms = allCodes[codes[0]];
		rooms.sort(sortNum);
		
		// add building codes to the building select
		for (var i=0; i<codes.length; i++) {
			$("#build").append( $(new Option(codes[i], codes[i])) );
		}
		// initialize the room select with the first building's rooms
		for (var i=0; i<rooms.length; i++) {
			$("#roomnum").append( $(new Option(rooms[i], rooms[i])) );
		}
	});


	$("#build").change(function() {
		//makes the combobox possible - upon changing the building select, removes all room numbers in
		//the roomnumber select and adds the ones for the new building
		$("#roomnum").empty();
		var rooms = allCodes[$("#build").val()]; //["145", "150"...]
		rooms.sort(sortNum);
		for (var i=0; i<rooms.length; i++) {
			$("#roomnum").append( $(new Option(rooms[i], rooms[i]) ) );
		}
	});
	
	// checking when a specified room is free
	$('#gettimes').click(function() {

		var room = $("#build").val() + " " + $("#roomnum").val(),

			timeReq = $.ajax({
				url: "http://127.0.0.1:5000/roomsurfer",
				type: 'POST',
				data: JSON.stringify({'room': room, 'type': 'ROOM'})
			});

		timeReq.done(function(data) {
			data = JSON.parse(data);
			var theTimes = [convertToTimes(data['M']),convertToTimes(data['T']),convertToTimes(data['W']),convertToTimes(data['Th']),convertToTimes(data['F'])];

			if ($("#freetimeinfo").is(':visible')) {

				$("#desctimes").html("<strong>"+room+"</strong> is available at:");
				for (var i=0; i < days.length; i++) {   //update each of the day <span> tags with times
					$("#" + days[i]).html("<strong>"+days[i]+"</strong><br>" + theTimes[i].join("<br>"));
				}

			} else {

				$("#desctimes").html("<strong>"+room+"</strong> is available at:");
				for (var i=0; i < days.length; i++) {   //update each of the day <span> tags with times
					$("#" + days[i]).html("<strong>"+days[i]+"</strong><br>" + theTimes[i].join("<br>"));
				}
				$("#desctimes").delay(200).fadeIn(400);
				$("#freetimeinfo").delay(200).fadeIn(400);
			}
		});
	});

	// checking what rooms are free at a specified time interval
	$("#getrooms").click(function() {
		var starttime = Number($("#starttime").val()),
			endtime = Number($("#endtime").val()),
			day = $("#day").val();
		if (starttime > endtime) {

			$("#descrooms").text("Please enter a valid time interval.");
			if (!$("#descrooms").is(":visible")) {
				$("#descrooms").fadeIn(400);
			}

		} else {

			var time = [starttime.toString(), endtime.toString(), day].join(),

				roomReq = $.ajax({
					url: 'http://127.0.0.1:5000/roomsurfer',
					type: 'POST',
					data: JSON.stringify({'time': time, 'type': 'TIME'})
				});

			roomReq.success(function(data) {
				data = JSON.parse(data);
				var buildings = Object.keys(data);
				buildings.sort();

				if (buildings.length === 0) {

					$("#descrooms").text("There aren't any rooms available at that time. What a shame.");
					if (!$("#descrooms").is(":visible")) {
						$("#descrooms").fadeIn(400);
					}

				} else {

					$("#descrooms").html("The following rooms are available at <strong>"
						+ converttoclock(starttime) + " - " + converttoclock(endtime) + "</strong> \
						on <strong>" + dayname(day) + "</strong>:<br><br>");

					for (var i=0; i<buildings.length; i++) {
						var buildingRooms = data[buildings[i]];
						buildingRooms.sort();
						$("#descrooms").append("<h4>"+ buildings[i] +"</h4><p>"+ buildingRooms.join(", ") + "</p>");
					}

					if (!$("#descrooms").is(":visible")) {
						$("#descrooms").delay(100).fadeIn(400);
					}
				}
			});
		}
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
			$("#desctimes").html("");
			for (var i=0; i < days.length; i++) {    //remove the text from each of the day <span> tags
				$("#" + days[i]).html("");
			}
		});
		$("#desctimes").fadeOut(500);
		$("#freetimeinfo").fadeOut(500);
	});

	$("#times-to-rooms").click(function() {
		$("#times").fadeOut(500);
		$("#times-to-rooms").fadeOut(500, function() {
			$("#rooms").fadeIn(500);
			$("#rooms-to-times").fadeIn(500);
			$("#descrooms").html("");
			$("#desctimes").fadeOut(500);
		});
	});
});
