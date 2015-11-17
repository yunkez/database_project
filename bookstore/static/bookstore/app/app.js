app = angular.module('myApp', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller( 'AppController', ['$scope', '$http', function($scope, $http) {
    $scope.test = "abc";
}])