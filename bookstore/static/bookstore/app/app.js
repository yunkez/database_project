app = angular.module('myApp', ['ui.bootstrap'])

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller( 'AppController', ['$scope','$modal', '$http', function($scope,$modal, $http) {
    $http.get('/bookstore/all_books').success(function(response) {
        $scope.book_list = response;
    });

    $scope.openBookModal = function(book){
    	var modalInstance = $modal.open({
            templateUrl: 'BookDetailModal.html',
            controller: 'ModalCtrl',
            resolve: {
                params: function () {
                    return book;
                }
            }
    	})
    };


}]);

app.controller('ModalCtrl', ['$scope', '$modalInstance', 'params', function($scope, $modalInstance, params){
	$scope.c = params;
	$scope.ok = function () {
        $modalInstance.close();
    };

    $scope.cancel = function () {
        $modalInstance.dismiss();
    };
}]);
