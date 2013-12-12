(function() {
    'use strict';

    angular.module('version_hub')
    .directive('rxNotifications', function () {
        return {
            restrict: 'E',
            templateUrl: '/views/directives/rx-notifications.html',
            scope: {
                application: '=',
                environment: '='
            }
        };
    });

})();