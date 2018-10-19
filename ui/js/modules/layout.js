define(['jquery', 'underscore', 'postal', 'w2ui'], function requireLayouts($, _, ps) {
    function Layout(layoutName, layoutSelector, config) {
        var that = this;
        this.layoutId = _.uniqueId();
        this.name = layoutName;
        this.selector = layoutSelector;
        this.config = config;
        this.w2ui;
    }

    Layout.prototype = {
        constructor: Layout,
        createLayout: function createLayout() {
            $(this.selector).w2layout(this.config);
            this.w2ui = w2ui[this.config.name];

            ps.publish({
                channel: 'layouts',
                topic: 'loaded.' + this.name,
                data:  this.w2ui
            });
        },
        on: function on(event, callback) {
            w2ui[this.name].on(event, function layoutEventCallback(layout, event) {
                if (callback) {
                    callback(event);
                }

                event.done(function eventDone(e) {
                    ps.publish({
                        channel: 'layout',
                        topic: 'event.' + event.type + '.' + layout,
                        data: event
                    });
                });
            });
        }
    };

    return Layout;
});
