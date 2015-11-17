app = angular.module('myApp', [])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller( 'AppController', ['$scope', '$http', function($scope, $http) {
    $scope.showModal = true;
    $http.get('/bookstore/all_books').success(function(response) {
        $scope.book_list = response;
    });

    $scope.toggleModal = function(){
        $scope.showModal = !$scope.showModal;
    };


}]);
