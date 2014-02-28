(function() {
    'use strict';

    angular.module('version_hub', ['ngRoute', 'ngResource', 'encore.ui', 'applications'])
        .constant('ROUTE_PATHS', {
            'homepage': '/',
            'applications': '/applications',
            'application': '/applications/:applicationid'
        })
        .config(function($routeProvider, ROUTE_PATHS) {
            $routeProvider
                .when(ROUTE_PATHS.applications, {
                    templateUrl: 'views/applications.html',
                    controller: 'ApplicationsCtrl'
                })
                .when(ROUTE_PATHS.application, {
                    templateUrl: 'views/applicationDetails.html',
                    controller: 'ApplicationDetailsCtrl'
                })
                .otherwise({
                    redirectTo:ROUTE_PATHS.applications
                });
        });
})();