var roomsurferControllers = angular.module('roomsurferControllers', []);

function convertTo12H(N) {
    // give a number of minutes, convert it to a 12-hour clock
    var period = (N < 720) ? 'AM' : 'PM';
    N = (N >= 780) ? N - 12*60 : N;

    var hour = Math.floor(N/60).toString(),
        min = (N%60).toString();

    if (parseInt(min,10) < 10)
        min = '0' + min;

    return hour + ':' + min + ' ' + period;
}

function stripTime(S) {
    // URL-izes time, e.g.  8:30 AM --> 830AM
    return S.replace(/[\s:]/g, '');
}

function convertToMins(S) {
    // converts 12h clock to minutes; usually of form e.g. '8:30 AM'
    var min, hour, period;
    S = stripTime(S);

    if (S.length === 5)
        hour = parseInt(S.slice(0,1));
    else
        hour = parseInt(S.slice(0,2));

    min = parseInt(S.slice(-4,-2));
    period = S.slice(-2);
    
    if (hour < 12 && period === 'PM')
        hour += 12;

    return 60*hour + min;
}

function validURLStartTime(S) {
    // given URL-ized (start) time, checks if it's valid within time constraints
    // e.g. 830AM --> true, LOLAM --> false
    var p;
    if (S.length === 5)
        p = /^([89][03]0AM|[1-7][03]0PM)$/;
    else if (S.length === 6)
        p = /^1([01][03]0AM|2[03]0PM)$/;
    else
        return false;

    return p.test(S);
}

function validURLEndTime(S) {
    var p;
    if (S.length === 5)
        p = /^(9[25]0AM|[1-9][25]0PM)$/;
    else if (S.length === 6)
        p = /^1([01][25]0AM|2[25]0PM)$/;
    else
        return false;

    return p.test(S);
}

function validURLDay(S) {
    if (S.length > 2)
        return false;

    return /(M|T|W|Th|F)/.test(S);
}


roomsurferControllers.controller('timesCtrl', ['$scope', '$routeParams', 'Building', 'Times',
    function ($scope, $routeParams, Building, Times) {

        $scope.convertTo12H = convertTo12H;

        $scope.changeCode = function() {
            // update roomnumbers select when building changes; remove previous search
            $scope.rooms = $scope.buildings[$scope.b];
            $scope.num = $scope.rooms[0];
            $scope.searching = $scope.invalidInput = false;
        }

        $scope.changeNum = function() {
            // remove previous search if it existed
            $scope.searching = $scope.invalidInput = false;
        }

        $scope.getTimes = function(building, num) {
            // get the free times for the selected room
            // this function is called both via button click and via direct URL
            Times.get({roomId: [building, num].join("-")}, function(data) {
                if (!data.hasOwnProperty('info')) {
                    // user accesses Roomsurfer with faulty input (via URL directly)
                    $scope.invalidInput = true;
                } else {
                    data = data.info;
                    $scope.b = building;
                    $scope.rooms = $scope.buildings[building];
                    $scope.num = num;
                    $scope.times = [{day:'Monday',data:data.M}, {day:'Tuesday',data:data.T}, {day:'Wednesday',data:data.W}, 
                                    {day:'Thursday',data:data.Th}, {day:'Friday',data:data.F}];
                    $scope.searching = true;
                    $scope.invalidInput = false;
                }
            });
        }

        $scope.searching = false;
        $scope.invalidInput = false;
        $scope.times = new Array(5);
        
        Building.query({}, function(data) {
            // called when any route is accessed; populates building select
            $scope.buildings = {};
            data.forEach(function(o) {
                $scope.buildings[o.building] = o.rooms;
            });
            $scope.b = data[0].building;
            $scope.rooms = data[0].rooms;
            $scope.num = $scope.rooms[0];
        });

        if ($routeParams.hasOwnProperty('room')) {
            // NOTE: the view's button redirects the user to #/rooms/:roomId, which re-renders the view
            // but we grab the parameter and call the function as needed. I'm tired.
            var room = $routeParams.room.split("-");
            $scope.getTimes(room[0], room[1]);
        }
    }
]);

roomsurferControllers.controller('roomsCtrl', ['$scope', '$routeParams', 'Rooms',
    function ($scope, $routeParams, Rooms) {

        $scope.convertToMins = convertToMins;
        $scope.stripTime = stripTime;
        
        $scope.getRooms = function(err, start, end, day) {
            // get the free rooms for the selected time

            // url-parameter is not of the correct form
            if (err) {
                $scope.invalidInput = true;
                $scope.startTime = '8:30 AM';
                $scope.endTime = '9:50 AM';
                $scope.day = 'M';
                return;
            }

            Rooms.get({timeId: [start, end, day].join('-')}, function(data) {
                if (!data.hasOwnProperty('info')) {
                    $scope.noRooms = true;
                } else {
                    data = data.info;
                    data.forEach(function(el) {
                        el = el.split(" ");
                        var b = el[0],
                            n = el[1];
                        if ($scope.rooms.hasOwnProperty(b))
                            $scope.rooms[b].push(n);
                        else
                            $scope.rooms[b] = [n];
                    });
                    $scope.searching = true;
                }
                $scope.startTime = convertTo12H(start);
                $scope.endTime = convertTo12H(end);
                $scope.day = day;
            });
        }

        $scope.changeSelect = function() {
            // checks to see if the button should be disabled or not
            // also removes previous searches
            $scope.disableBtn = (convertToMins($scope.startTime) - convertToMins($scope.endTime) >= -20) ? true : false;
            $scope.searching =  $scope.invalidInput = $scope.noRooms = false;
        }

        $scope.rooms = {};
        $scope.dayAbbreviations = {M: 'Monday', T: 'Tuesday', W: 'Wednesday', Th: 'Thursday', F: 'Friday'};
        $scope.disableBtn = false;
        
        // initialize selects
        $scope.startTimes = new Array(22);
        $scope.endTimes = new Array(26);
        $scope.days = ['M', 'T', 'W', 'Th', 'F'];

        for (var i=0; i<22; i++) {
            $scope.startTimes[i] = convertTo12H(510 + 30*i);
            $scope.endTimes[i] = convertTo12H(560 + 30*i);
        }
        for (i=22; i<26; i++)
            $scope.endTimes[i] = convertTo12H(560 + 30*i);

        $scope.startTime = $scope.startTimes[0];
        $scope.endTime = $scope.endTimes[0];
        $scope.day = $scope.days[0];

        if ($routeParams.hasOwnProperty('time')) {
            // same idea applies.
            var time = $routeParams.time.split('-'),
                start = time[0],
                end = time[1],
                day = time[2];
            if (end === undefined || day === undefined)
                $scope.getRooms(true);
            else if (!validURLStartTime(start) || !validURLEndTime(end) || !validURLDay(day))
                $scope.getRooms(true);
            else
                $scope.getRooms(false, convertToMins(start),convertToMins(end),day);
        }
    }
]);