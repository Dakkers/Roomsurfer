function converttoclock(m) {
	//given a number of minutes, converts to 12-hour clock
	if (m >= 780) {
		//780 mins = 13 hours = 1 PM
		var when = 'PM';
		m = m - 12*60
	} else if (m >= 720 && m < 780) {
		var when = 'PM';
	} else {
		var when = 'AM';
	}

	var hour = Math.floor(m/60).toString(), min = (m%60).toString();

	if (parseInt(hour) < 10) {	hour = '0' + hour; 	}
	if (parseInt(min) < 10) { 	min = '0' + min;	}

	return hour + ':' + min + ' ' + when;
}

function convertallthethings(L) {
	//given an array of arrays (of two ints (start/endtimes))
	//returns the time interval in a 12-hour clock format for each
	L_return = [];
	for (var i=0; i < L.length; i++) {
		var l = L[i];
		var st = converttoclock(l[0]), et = converttoclock(l[1]);
		var interval = st + ' - ' + et;
		L_return.push(interval);
	}
	return L_return;
}

function gettimes(justthrowthecakeuphereplease, key) {
	//given a room code (building+number), returns all times that the room is free (in a clock fashion)
	//note that justthrowthecakeuphereplease = the master dictionary of all times! because global vars are for the devil
	//http://www.youtube.com/watch?v=pX4SQcqHW5k
	var room = justthrowthecakeuphereplease['freetimes_sorted'][key];
	var M = room["M"], T = room["T"], W = room["W"], Th = room["Th"], F = room["F"];
	M = convertallthethings(M), T = convertallthethings(T), W = convertallthethings(W);
	Th = convertallthethings(Th), F = convertallthethings(F);
	return [M, T, W, Th, F];
}

function getfreerooms(dict, timearray) {
	var time = timearray.join(',');
	return dict[time];
}

function dayname(abbrv) {
	var hmph = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'Th': 'Thursday', 'F': 'Friday'};
	return hmph[abbrv];
}

function sortNum(a,b) {
	return a - b;
}


$(document).ready(function () {
	var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

	$("#header").hide().fadeIn(600);
	$("#splash").hide().fadeIn(800);

	var masterdict = {}; //too used to thinking of these as Python dictionaries
	$.getJSON("http://stdako.com/1141times.json", function(data) {
		$.each(data, function(key,val) {
			masterdict[key] = val;
		});
	});

	var allcodes = {}; //format: {"PHY": ["145", "150", ...], ...}

	function updateselects() {
		//add all of the buildings used this term to the Building select box
		allcodes = {};
		var fts = masterdict["freetimes_sorted"];
		var codes = Object.keys(fts);
		codes.sort();
		$("#build").empty();

		for (var i=0; i<codes.length; i++) {
			var b = codes[i].split(" ")[0], num = parseInt(codes[i].split(" ")[1]);
			if (!(allcodes.hasOwnProperty(b))) {
				allcodes[b] = [num]
				$("#build").append( $(new Option(b, b) ) );
			} else {
				allcodes[b].push(num);
			}
		}
	}

	$("#build").change(function() {
		//makes the combobox possible - upon changing the building select, removes all room numbers in
		//the roomnumber select and adds the ones for the new building
		$("#roomnum").empty();
		var rooms = allcodes[$("#build").val()]; //["145", "150"...]
		rooms.sort(sortNum);
		for (var i=0; i<rooms.length; i++) {
			$("#roomnum").append( $(new Option(rooms[i], rooms[i]) ) );
		}
	});
	 
	$('#gettimes').click(function() {
		//var room = $("#giveroom").val().toUpperCase(); //make sure user doesn't put in lowercase room name
		var fts = masterdict["freetimes_sorted"];
		var room = $("#build").val() + " " + $("#roomnum").val();

		if (fts.hasOwnProperty(room)) {
			the_times = gettimes(masterdict, room); //I am so hungry

			if ($("#freetimeinfo").is(':visible')) {

				$("#desctimes").html("<strong>"+room+"</strong> is available at:");
				for (var i=0; i < days.length; i++) {   //update each of the day <span> tags with times
					$("#" + days[i]).html("<strong>"+days[i]+"</strong><br>" + the_times[i].join("<br>"));
				}

			} else {

				$("#desctimes").html("<strong>"+room+"</strong> is available at:");
				for (var i=0; i < days.length; i++) {   //update each of the day <span> tags with times
					$("#" + days[i]).html("<strong>"+days[i]+"</strong><br>" + the_times[i].join("<br>"));
				}
				$("#desctimes").delay(200).fadeIn(400);
				$("#freetimeinfo").delay(200).fadeIn(400);
			}

		} else {

			if (!$("#freetimeinfo").is(":visible")) {
				$("#desctimes").delay(200).fadeIn(400);
				$("#freetimeinfo").delay(200).fadeIn(400); //this could be better... but I don't care
			}

			$("#desctimes").html("That isn't in the database. Perhaps you didn't enter it correctly, \
				or perhaps it is always free - but what's more likely?"); //code needs to be sassy
			for (var i=0; i < days.length; i++) {    //remove the text from each of the day <span> tags
				$("#" + days[i]).html("");
			}
		}
	});

	$("#getrooms").click(function() {
		var ft = masterdict["freerooms"];
		var starttime = Number($("#starttime").val()), endtime = Number($("#endtime").val()), day = $("#day").val();
		if (starttime > endtime) {

			$("#descrooms").text("Please enter a valid time interval.");
			if (!$("#descrooms").is(":visible")) {
				$("#descrooms").fadeIn(400);
			}

		} else {

			var interval = [starttime.toString(), endtime.toString(), day];
			var freerooms = getfreerooms(ft, interval);
			if (freerooms.length === 0) {

				$("#descrooms").text("There aren't any rooms available at that time. What a shame.");
				if (!$("#descrooms").is(":visible")) {
					$("#descrooms").fadeIn(400);
				}

			} else {

				var temp = {}; //format: {"BUILDING": [100, 150, 175]}
				for (var i=0; i<freerooms.length; i++) {
					var b = freerooms[i].split(" ")[0], num = freerooms[i].split(" ")[1];
					if (!(temp.hasOwnProperty(b))) {
						temp[b] = [num];
					} else {
						temp[b].push(num);
					}
				}

				$("#descrooms").html("The following rooms are available at <strong>" + converttoclock($("#starttime").val()) + " - " + converttoclock($("#endtime").val()) + "</strong> \
					on <strong>" + dayname(day) + "</strong>:<br><br>");
				for (var key in temp) {
					$("#descrooms").append("<h4>"+ key +"</h4><p>"+ temp[key].join(", ") + "</p>");
				}
				if (!$("#descrooms").is(":visible")) {
					$("#descrooms").delay(100).fadeIn(400);
				}
			}
		}
	});


	$("#splashtimes").click(function() {
		updateselects();
		$("#splash").fadeOut(500);
		$("#times").delay(800).fadeIn(500);
		$("#times-to-rooms").delay(800).fadeIn(500);
	});

	$("#splashrooms").click(function() {
		$("#splash").fadeOut(500);
		$("#rooms").delay(800).fadeIn(500);
		$("#rooms-to-times").delay(800).fadeIn(500);
	});

	$("#rooms-to-times").click(function() {
		updateselects();
		$("#roomnum").empty();
		$("#rooms").fadeOut(500);
		$("#rooms-to-times").fadeOut(500);
		$("#times").delay(500).fadeIn(500);
		$("#times-to-rooms").delay(500).fadeIn(500);
		$("#desctimes").html("");
		for (var i=0; i < days.length; i++) {    //remove the text from each of the day <span> tags
			$("#" + days[i]).html("");
		}
		$("#desctimes").fadeOut(500);
		$("#freetimeinfo").fadeOut(500);
	});

	$("#times-to-rooms").click(function() {
		$("#times").fadeOut(500);
		$("#times-to-rooms").fadeOut(500);
		$("#rooms").delay(500).fadeIn(500);
		$("#rooms-to-times").delay(500).fadeIn(500);
		$("#descrooms").html("");
		$("#desctimes").fadeOut(500);

	});	
});