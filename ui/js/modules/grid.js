define(['jquery', 'underscore', 'postal'], function requireGrids($, _, ps) {
    function Grid(gridName, gridSelector, config) {
        var that = this;
        this.gridId = _.uniqueId();
        this.name = gridName;
        this.selector = gridSelector;
        this.config = config;
        this.grid;
        var fusion = ps.channel('fusion');
        this.gridReady = $.Deferred();

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
            var $grid = $(that.selector);

            if (that.config.showSearchInColumns) {
                addColumnSearchControls(that.config.columns);
            }

            $grid.w2grid(that.config);
            that.grid = w2ui[that.config.name];
            that.gridReady.resolve();
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