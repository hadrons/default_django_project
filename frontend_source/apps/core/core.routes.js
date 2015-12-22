(function () {
    'use strict';

    angular
        .module('app')
        .config(routes);

    /* @ngInject */
    function routes ($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('home', {
                url: '/home',
                template: '<h1>Welcome to {{ vm.homeland }}</h1>',
                controller: 'HomeController as vm'
            });

        $urlRouterProvider
            .otherwise('/home');
    }
}());
