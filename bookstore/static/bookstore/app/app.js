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
            controller: 'BookDetailModalCtrl',
            resolve: {
                params: function () {
                    return book;
                }
            }
        });
        modalInstance.result.then(
			function (result) {
				
			},
			function (result) {
			}
		);

    };


}]);

app.controller('BookDetailModalCtrl', ['$scope', '$modalInstance', 'params', function($scope, $modalInstance, params){
	$scope.c = params;
	$scope.ok = function () {
        $modalInstance.close('this is result for close');
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('this is result for dismiss');
    };
}]);
