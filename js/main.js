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
		var st = converttoclock(L[i][0]), et = converttoclock(L[i][1]);
		var interval = st + ' - ' + et;
		L_return.push(interval);
	}
	return L_return;
}


$(window).load(function() {

	var mapper = {"r": "rooms", "t": "times"};

	$("#header").fadeIn(600);
	$("#main").fadeIn(800);

	$(".btn-main").click(function() {
		var div = mapper[$(this).attr('id').replace("btn-main-", "")];
		$("#main").fadeOut(400, function() {
			$("#"+div).fadeIn(400);
		});
	});

});