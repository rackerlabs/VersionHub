(function() {
    'use strict';

    angular.module('applications', [])
        .controller('ApplicationDetailsCtrl', function($scope, $routeParams, Applications,
            Dependencies, Versions, Notifications) {

            $scope.environments = [
                {name: 'Staging', value: 'staging' },
                {name: 'Production', value: 'production' }
            ];

            $scope.applications = [
                {name: 'Dbaas', value: 'staging' },
                {name: 'Dbaas', value: 'production' },
                {name: 'Lbaas', value: 'staging' },
                {name: 'Lbaas', value: 'production' }
            ];

            $scope.actions = {
                'addDependency': ['addDependency'],
            };

            $scope.environment = $scope.environments[0];
            $scope.addDependency = $scope.environments[0];

            $scope.tabs = [
                { title: 'Notifications', content: '<rx-notifications></rx-notifications>'},
                { title: 'Dependencies', content: '<rx-dependencies></rx-dependencies>'},
                { title: 'Version Log', content: '<rx-versionLog></rx-versionLog>'},
                // { title: 'Version Source', content: '<rx-versionSource></rx-versionSource>'}
            ];

            $scope.loadApplication = function() {
                var loadSuccess = function(data) {
                    $scope.application = data.application[0];
                };

                var loadFail = function(data) {
                    console.log(data);
                    console.log('Failure');
                };

                Applications.get({applicationid: $routeParams.applicationid}, loadSuccess, loadFail);
            };

            $scope.loadDependencies = function() {
                var loadSuccess = function(data) {
                    $scope.dependencies = data.dependencies;
                };

                var loadFail = function(data) {
                    console.log(data);
                    console.log('Failure');
                };

                Dependencies.get({applicationid: $routeParams.applicationid}, loadSuccess, loadFail);
            };

            $scope.loadVersions = function() {
                var loadSuccess = function(data) {
                    $scope.versions = data.versions;
                };

                var loadFail = function(data) {
                    console.log(data);
                    console.log('Failure');
                };

                Versions.get({applicationid: $routeParams.applicationid}, loadSuccess, loadFail);
            };

            $scope.loadNotifications = function() {
                var loadSuccess = function(data) {
                    $scope.notifications = data.notifications;
                };

                var loadFail = function(data) {
                    console.log(data);
                    console.log('Failure');
                };

                Notifications.get({applicationid: $routeParams.applicationid}, loadSuccess, loadFail);
            };

            $scope.loadApplication();
            $scope.loadDependencies();
            $scope.loadNotifications();
            $scope.loadVersions();
        });
})();