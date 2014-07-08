converttoclock = (m) ->
	period = ''
	if m >= 780
		period = 'PM'
		m = m - 12*60
	else if m >= 720 and m < 780
		period = 'PM'
	else
		period = 'AM'

	hour = Math.floor(m/60).toString()
	min = (m%60).toString()

	if parseInt(hour,10) < 10
		hour = '0' + hour
	if parseInt(min) < 10
		min = '0' + min

	return hour + ':' + min + ' ' + period

converttoint = (time) ->
	return null

convToTimes = (L) ->
	Lreturn = []
	for l in L
		st = converttoclock(l[0])
		et = converttoclock(l[1])
		interval = st + ' - ' + et
		Lreturn.append(interval)
	return Lreturn

dayname = (abbrv) ->
	hmph = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'Th': 'Thursday', 'F': 'Friday'}
	return hmph[abbrv]

