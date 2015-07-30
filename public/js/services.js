var roomsurferServices = angular.module('roomsurferServices', ['ngResource']);

roomsurferServices.factory('Building', ['$resource',
    function ($resource){
        return $resource('/roomsurfer/api/usedrooms/', {}, {
            query: {method:'GET', isArray: true}
        });
    }
]);

roomsurferServices.factory('Times', ['$resource', 
	function ($resource) {
		return $resource('/roomsurfer/api/room/:building/:room', {}, {
			query: {method: 'GET', isArray: true}
		});
	}
]);

roomsurferServices.factory('Rooms', ['$resource',
	function ($resource) {
		return $resource('/roomsurfer/api/time/:day/:start/:end', {}, {
			query: {method: 'GET', isArray: true}
		});
	}
]);