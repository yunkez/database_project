app = angular.module('myApp', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller( 'AppController', ['$scope', '$http', function($scope, $http) {
    $http.get('/bookstore/all_books').success(function(response) {
    	$scope.book_list = response;
    	// $scope.list = response;
    });

    // $scope.list = $scope.book_list;
    $scope.config = {
    	itemsPerPage: 10,
    	fillLastPage: true
    }

}])