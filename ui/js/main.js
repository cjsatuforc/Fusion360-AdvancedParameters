/* global requirejs */

requirejs.config({
    baseUrl: 'js',
    paths: {
        jquery: 'lib/jquery-3.3.1.min',
        underscore: 'lib/underscore-min',
        w2ui: 'lib/w2ui-1.5.rc1.min',
        pubsub: 'lib/pubsub',
        postal: 'lib/postal.min',
        'postal.request-response' : 'lib/postal.request-response.min',
        lodash: 'lib/lodash.min',
        text: 'lib/text'
    },
    shim: {
        underscore: {
            exports: '_'
        },
        w2ui: ['jquery']
    }
});

require(['app', 'jquery', 'postal', 'postal.request-response', './modules/debugger'], function appMain(app, $, ps) {
    // We have to tell postal how to get an deferred instance
    ps.configuration.promise.createDeferred = function() {
        return new $.Deferred();
    };
    // We have to tell postal how to get a "public-facing"/safe promise instance
    ps.configuration.promise.getPromise = function(dfd) {
        return dfd.promise();
    };

    app.init();
});
