(function() {
    'use strict';

    var api = {};
    api.applications  = '/api/applications/:applicationid';
    api.versions      = api.applications + '/versions';
    api.notifications = api.applications + '/notifications/:notificationid';
    api.dependencies  = api.applications + '/dependencies/:dependencyid';

    angular.module('version_hub')
        .factory('Applications', function($resource) {
            return $resource(api.applications);
        })
        .factory('Versions', function($resource) {
            return $resource(api.versions);
        })
        .factory('Notifications', function($resource) {
            return $resource(api.notifications);
        })
        .factory('Dependencies', function($resource) {
            return $resource(api.dependencies);
        });
})();