define(['postal', 'jquery', 'underscore'], function requireData(ps, $, _) {
    var rip = {};
    var fusionReady = false;
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
                    fusionReady = true;
                    fusionIsReady();
                } else if (command.indexOf('isReady') === 0 ) {
                    fusionIsReady();
                }
            }
        });

        window.fusionJavaScriptHandler = {
            handle: function(requestAction, data){
                var action = $.parseJSON(requestAction);
                var response = $.parseJSON(data);

                var responseId = action.responseId;
                var rip = getRip(responseId);

                // alert('command sent from fusion!!!');
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

        /*
            if (!adsk) {
                adsk = {
                    fusionSendData: function fusionSendData(command) {
                        if (command.command === 'get') {
                            setTimeout(function() {
                                $.ajax({
                                    type: 'GET',
                                    dataType: 'html',
                                    url: 'data.parameters.json',
                                    success: function (response) {
                                        window.fusionJavaScriptHandler.handle(command, response);
                                    }
                                });

                            }, 3000);
                        } else {
                            setTimeout(function() {
                                var response = JSON.stringify({ status: 'success' });
                                window.fusionJavaScriptHandler.handle(command, response);
                            });
                        }
                    }
                };
            }
        */
    };

    var fusionIsReady = function fusionIsReady() {
        if (fusionReady === true) {
            sendFusionResponse('',
                {
                    channel: 'fusion',
                    topic: 'ready'
                });

        }
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

        $('#messages').prepend('<p>Sent: command = ' + JSON.stringify(action) + '</p>');

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