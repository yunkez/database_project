app = angular.module('myApp', [])

app.controller( 'AppController', ['$scope', '$http', function($scope, $http) {
    $scope.test = "abc";
}])