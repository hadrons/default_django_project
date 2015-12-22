(function () {
    'use strict';

    angular
        .module('app.example')
        .config(routes);

    /* @ngInject */
    function routes ($stateProvider) {
        $stateProvider
            .state('example', {
                url: '/example',
                templateUrl: 'apps/example/example.html',
                controller: 'ExampleController as vm'
            });
    }
}());
