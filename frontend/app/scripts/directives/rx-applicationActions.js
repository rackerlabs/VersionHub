angular.module('applications')
    .directive('rxDatabaseActions', function() {
        return {
            restrict: 'E',
            transclude: true,
            scope: {
                status: '=',
                actions: '='
            },
            templateUrl: '/views/applicationActions/rx-applicationActions.html',
            controller: function ($scope) {

                //var defaultSvcParams = {};

                $scope.displayAction = function (actionName) {
                    return _.indexOf($scope.actions, actionName) > -1;
                };

                // Create Database
                $scope.addDependency = {
                    preHook: function (modalScope) {
                        modalScope.fields = {};
                    }//,
                    // postHook: function(fields) {
                    //     var addSuccess = function () {
                    //         $scope.status = Flash.set('Adding Appliction.');
                    //         $route.reload(); // Reload current view
                    //     };

                    //     var addFailure = function () {
                    //         $scope.status = Status.setMsg('Error adding application.', false);
                    //     };

                    //     var db = fields.database;
                    //     var createData = {
                    //         'application': ''
                    //     };

                    //     /* jshint camelcase: false */
                    //     createData.databases[0].application_id = app.id;
                        
                        //Dbaas.createDatabase(defaultSvcParams, createData, addSuccess, addFailure);
                    //}
                };
            }
        };
    });