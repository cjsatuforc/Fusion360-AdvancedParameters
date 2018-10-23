define(['postal', 'jquery', 'underscore'], function requireData(ps, $, _) {
    var rip = {};
    var fusionReady = $.Deferred();
    var defaultTimeout = 5000;
    var adsk = adsk || undefined;


    var init = function init() {
        ps.subscribe({
            channel: 'fusion',
            topic: '#',
            callback: function fusionCommandCallback(action, envelope) {
                var command = envelope.topic;

                if (command.indexOf('get')  === 0 ||
                    command.indexOf('set') === 0) {

                    action.command = envelope.topic;

                    sendToFusion(action, envelope).then(
                        function sendToFusionCallback(data) {
                            if (envelope.reply) {
                                envelope.reply(null, data);
                            } else {
                                sendFusionResponse(data);
                            }
                        });
                } else if (command.indexOf('init') === 0 ) {
                    var reqTopic = envelope.topic.split('.')[1];
                    fusionReady.resolve();

                    if (reqTopic) {
                        fusionIsReady(reqTopic);
                    }

                } else if (command.indexOf('isReady') === 0 ) {
                    fusionIsReady(envelope.topic.split('.')[1]);
                }
            }
        });

        window.fusionJavaScriptHandler = {
            handle: function(requestAction, data){
                var action = $.parseJSON(requestAction);
                var response = $.parseJSON(data);

                var responseId = action.responseId;
                var rip = getRip(responseId);

                $('#messages').prepend('<p>Recieved: action = ' + requestAction + ' | data = ' + data + '</p>');
                if (rip) {
                    rip.resolve(response);
                    deleteRip(responseId);
                } else {
                    sendFusionResponse(data,
                        {
                            channel: action.channel,
                            topic: action.topic
                        });
                }

                return 'OK';
            }
        };
    };

    var fusionIsReady = function fusionIsReady(reqTopic) {
        if (fusionReady.state() === 'pending') {
            if (window.adsk && window.fusionJavaScriptHandler.handle) {
                fusionReady.resolve();
            }
        }

        fusionReady.then(function fusionReady() {
            var topic = reqTopic ? 'ready.' + reqTopic : 'ready';
            sendFusionResponse('',
                {
                    channel: 'fusion',
                    topic: topic
                });
        });
    };

    var sendToFusion = function sendToFusion(action, envelope) {
        adsk = window.adsk;
        action.responseId = newRip();
        var d = getRip(action.responseId);
        var timeout = action.timeout;

        if (_.isUndefined(timeout)) {
            timeout = defaultTimeout;
        } else if (_.isBoolean(timeout)) {
            timeout = !timeout || defaultTimeout;
        } else if (!_.isNumber(timeout)) {
            timeout = false;
        }

        adsk.fusionSendData(JSON.stringify(action), JSON.stringify(envelope));
        $(function() {
            $('#messages').prepend('<p>Sent: command = ' + JSON.stringify(action) + '</p>');
        });

        if (timeout) {
            setTimeout(function getDataTimeout() {
                if (d && d.state() !== 'resolved') {
                    var errorMessage = 'Timed out while trying to get data.';

                    ps.publish({
                        channel: 'error',
                        topic: 'data.request',
                        data: { message: errorMessage, command: action, envelope: envelope }
                    });

                    d.resolve({ status: 'error', message: errorMessage, command: action, envelope: envelope });
                }
            }, timeout);
        }

        return d.promise();
    };

    var sendFusionResponse = function sendFusionResponse(data, envelope) {
        var channel = 'fusion.response';
        var topic = 'response';

        if (envelope) {
            channel = envelope.channel;
            topic = envelope.topic;
        }

        ps.publish({
            channel: channel,
            topic: topic,
            data: data
        });
    };

    var deleteRip = function deleteRip(id) {
        if (rip[id]) {
            delete rip[id];
        }
    };

    var newRip = function setRip() {
        var id = _.uniqueId();

        rip[id] = $.Deferred();
        return id;
    };

    var getRip = function getRip(id) {
        return rip[id];
    };

    return {
        init: init
    };

});