define(['jquery', 'underscore', 'postal', './grid', 'text!../../css/grid.css'], function requireParametersGrid($, _, ps, Grid, css) {
    $('head').append('<style>' + css + '</style>');
    var fusion = ps.channel('fusion');

    var config = {
        showSearchInColumns: true,
        name: 'parametersGrid',
        method: 'GET',
        recordHeight: 40,
        recid: 'name',
        columns: [
            {
                field: 'attribute-group',
                caption: 'Group',
                sortable: true,
                size: '25%',
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'name',
                caption: 'Name',
                sortable: true,
                size: '25%',
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'expression',
                caption: 'Expression',
                size: 250,
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'value',
                caption: 'Value',
                sortable: true,
                size: '25%'
            },
            {
                field: 'unit',
                caption: 'Unit',
                size: 25,
                searchType: 'select'
            },
            {
                field: 'comment',
                caption: 'Comment',
                size: 100
            }
        ]
    };

    var deferreds = [];

    var init = function init() {
        var g = new Grid(config.name, '#parameters', config);
        var layoutDef = $.Deferred();
        deferreds.push(layoutDef);

        ps.subscribe({
            channel: 'layouts',
            topic: 'loaded.layout1',
            callback: function layoutsLoadedGrid(layout, envelope) {
                layout.content('main', '<div id="parameters" style="width: 100%; height: 100%; overflow: hidden;"></div>');

                layoutDef.resolve();
            }
        }).once();

        ps.subscribe({
            channel: 'layout',
            topic: 'event.resize.layout1',
            callback: function layoutResized(msg, data) {
                var $grid = $(g.selector);
                var height = $grid.parent().height();
                $grid.outerHeight(height);
            }
        });

        fusion.subscribe({
            topic: 'ready.parameters',
            callback: function fusionReady(data, envelope) {
                if (g.gridReady.state() === 'resolved') {
                    g.grid.clear();
                    g.grid.lock('Loading parameters...', true);
                }

                fusion.request({
                    topic: 'get',
                    replyChannel: 'fusion.response',
                    data: {
                        item: 'parameters'
                    }
                }).then(
                    function gridDataReceived(data) {
                        // d.resolve(data);
                        g.gridReady.then(function gridReadyForData() {
                            g.grid.clear();
                            g.grid.add(data.records);
                            g.grid.unlock();
                        });
                    },
                    function gridDataError(error) {
                        // d.resolve({ status: 'error', msg: error });
                        g.grid.error(
                            'There was an error while trying to get grid data from Fusion 360. <br> Error message: ' + error
                        );
                    });
            }
        });

        fusion.publish({
            channel: 'fusion',
            topic: 'isReady.parameters'
        });

        $.when.apply($, deferreds).then(function() {
            g.createGrid();

            g.grid.lock('Loading parameters...', true);

            g.grid.on('change', function gridChange(event) {
                g.grid.lock('Saving to Fusion 360...', true);
                g.grid.status('Saving to Fusion 360');
                console.log('Grid Changed!');
                event.done(function(e) {
                    var record = g.grid.records[e.index];
                    var field = g.grid.columns[e.column].field;
                    var identifier = record.name;
                    var oldValue = e.value_previous;
                    var newValue = e.value_new;

                    if (field === 'name') {
                        identifier = oldValue;
                    }

                    fusion.request({
                        topic: 'set',
                        replyChannel: 'fusion.response',
                        data: {
                            item: 'parameters',
                            arguments: [
                                {
                                    name: identifier,
                                    field: field,
                                    value: newValue
                                }
                            ]
                        }
                    }).then(
                        function gridDataReceived(data) {
                            g.grid.unlock();
                            if (data.status === 'success') {
                                g.grid.save();
                            } else {
                                record.w2ui.changes = {};
                                g.grid.refresh();
                                g.grid.error(
                                    'There was an error while trying to save changes to Fusion 360. <br> Error message: ' + data.message
                                );
                            }
                        }
                    );
                });
                console.log('Grid change done');
            });

            g.grid.on('editField', function gridEditField(event) {
                if (event.originalEvent.keyCode === 13) {
                    event.preventDefault();
                }
            });

            g.grid.on('dblClick', function(event) {
                console.log('dblClick');
            });
        });
    };

    return {
        init: init
    };
});
