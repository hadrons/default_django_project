(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    /* @ngInject */
    function HomeController (logger) {
        var vm = this;
        vm.homeland = 'Hadrons';
        logger.log('Done loading everything... Success... o/');
    }
}());
