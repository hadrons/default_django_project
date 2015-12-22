(function () {
    'use strict';

    angular
        .module('app.example')
        .factory('Custom', Custom);

    /* @ngInject */
    function Custom ($localStorage, $q, Logger) {
        var
            LOCAL_CACHE_STORAGE = 'CustomCacheLocalStorage'
        ;
        return {
            getPersisted: getPersisted
            , persistLocal: persistLocal
            , clear: clear
        };

        function persistLocal (params) {
            Logger.log('Persisting Custom stuff...', params);

            $localStorage[LOCAL_CACHE_STORAGE] = $localStorage[LOCAL_CACHE_STORAGE] || {};
            angular.forEach(params, function (value, key) {
                $localStorage[LOCAL_CACHE_STORAGE][key] = value;
            });
        }

        function getPersisted () {
            var deferred = $q.defer();

            if ($localStorage[LOCAL_CACHE_STORAGE]) {
                deferred.resolve($localStorage[LOCAL_CACHE_STORAGE]);
            } else {
                deferred.reject('No loca Custom info');
            }

            return deferred.promise;
        }

        function clear () {
            var deferred = $q.defer();

            Logger.log('Clearing Custom local data');

            $localStorage[LOCAL_CACHE_STORAGE] = false;

            deferred.resolve();

            return deferred.promise;
        }
    }
}());
