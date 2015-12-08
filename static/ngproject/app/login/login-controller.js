/*TODO: define proqod module in upper level and just refer it here*/
angular.module("proqod", [])
.constant("loginUrl", "http://localhost:8000/auth/login/")
.controller("LoginCtrl", function($scope, $http, loginUrl) {
	$scope.login = function(user) {
		console.log(user);
		$http({
			method: "POST",
			url: loginUrl,
			data: user,
			headers: {
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': 'http://localhost:8000/auth/login/'
			}
		})
		.then(function(response) {
			console.log(response);
		}, function(response) {
			console.log(response);
		})
	}
})