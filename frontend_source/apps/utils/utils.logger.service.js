(function () {
    'use strict';

    angular
        .module('app.utils')
        .factory('Logger', Logger);

    function Logger () {
        var service = {
                log: log
            };

        return service;

        function log () {
            console.log(JSON.stringify(arguments));
        }
    }
}());
