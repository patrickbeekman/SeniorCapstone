// public/js/appRoutes.js
    angular.module('appRoutes', []).config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {

    $routeProvider

        // home page
        .when('/', {
            templateUrl: 'views/home.html',
            controller: 'MainController'
        })

        .when('/student', {
            templateUrl: 'views/student.html',
            controller: 'StudentController'
        })

        // nerds page that will use the NerdController
        .when('/nerds', {
            templateUrl: 'views/Tweet_freq_by_day.html',
            controller: 'BokehNerdController'
        });

    $locationProvider.html5Mode(true);

}]);


