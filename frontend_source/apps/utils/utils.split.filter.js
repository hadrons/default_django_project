(function () {
    'use strict';

    angular
        .module('app.utils')
        .filter('split', split);

    /* @ngInject */
    function split () {
        return function (input, splitChar, splitIndex) {
            return input.split(splitChar)[splitIndex];
        };
    }
}());
