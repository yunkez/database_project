app = angular.module('myApp', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller( 'AppController', ['$scope', '$http', function($scope, $http) {
    $http.get('/bookstore/json').success(function(response) {$scope.book_list = response;});
}])