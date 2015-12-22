(function () {
    'use strict';

    angular
        .module('app.example')
        .controller('ExampleController', ExampleController);

    /* @ngInject */
    function ExampleController () {
        var vm = this;

        vm.message = '';

        activate();

        function activate () {
            vm.message = 'Controller ';
        }
    }
}());
