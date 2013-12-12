(function() {
    'use strict';

    angular.module('version_hub')
        .controller('ApplicationsCtrl', function($scope, Applications) {
            
            $scope.loadApplications = function() {
                var loadSuccess = function(data) {
                    $scope.applications = data.applications;
                };

                var loadFail = function(data) {
                    console.log(data);
                    console.log('Failure');
                };

                Applications.get({}, loadSuccess, loadFail);
            };

            $scope.loadApplications();
        });
})();