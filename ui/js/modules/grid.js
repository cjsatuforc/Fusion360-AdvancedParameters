define(['jquery', 'underscore', 'postal'], function requireGrids($, _, ps) {
    function Grid(gridName, gridSelector, config) {
        var that = this;
        this.gridId = _.uniqueId();
        this.name = gridName;
        this.selector = gridSelector;
        this.config = config;
        this.w2ui;
        var fusion = ps.channel('fusion');
        this.gridDataReady = getGridData();

        function getGridData() {
            var d = $.Deferred();

            fusion.subscribe({
                channel: 'fusion',
                topic: 'ready',
                callback: function fusionReady() {
                    fusion.request({
                        topic: 'get',
                        replyChannel: 'fusion.response',
                        data: {
                            item: 'parameters'
                        }
                    }).then(
                        function gridDataReceived(data) {
                            d.resolve(data);
                        },
                        function gridDataError(error) {
                            d.resolve({ status: 'error', msg: error });
                        });
                }
            });

            fusion.publish({
                channel: 'fusion',
                topic: 'isReady'
            });

            return d.promise();
        }

        var addColumnSearchControls = function addFilterControls(columns) {
            var $newCaption;
            _.each(columns, function loopColumns(col, index) {
                if (col.searchType) {
                    $newCaption = $('<div></div>')
                        .append('<div>' + col.caption + '</div>')
                        .append('<input type="' + col.searchType + '" class="filter-control ' + col.caption + '"></input>');
                    col.caption = $newCaption.html();
                }
            });
        };

        this.createGrid = function createGrid() {
            var d = $.Deferred();
            var $grid = $(that.selector);

            if (that.config.showSearchInColumns) {
                addColumnSearchControls(that.config.columns);
            }

            $grid.w2grid(that.config);
            that.w2ui = w2ui[that.config.name];

            that.gridDataReady.then(function gridReady(data) {
                if (data.status === 'success') {
                    _.each(data.records, function (record) {
                        record.recid = record.ID;
                    });

                    that.w2ui.add(data.records);
                    d.resolve();
                } else {
                    $grid.html(data.msg + '<p>' + JSON.stringify(data.data) + '</p>');
                }
            });

            return d.promise();
        };
    }


    Grid.prototype = {
        constructor: Grid,
        on: function on(eventName, callback) {
            var that = this;
            that.gridDataReady.then(function bindEvent() {
                w2ui[that.name].on(eventName, function gridEventCallback(grid, event) {
                    if (callback) {
                        callback(event);
                    }

                    event.done(function eventDone(e) {
                        ps.publish({
                            channel: 'grid',
                            topic: 'event.' + event.type + '.' + this.name,
                            data: event
                        });
                    });
                });
            });
        }
    };

    return Grid;
});