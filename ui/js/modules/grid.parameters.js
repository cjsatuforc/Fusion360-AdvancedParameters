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
        var grid = new Grid(config.name, '#parameters', config);
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
                var $grid = $(grid.selector);
                var height = $grid.parent().height();
                $grid.outerHeight(height);
            }
        });

        $.when.apply($, deferreds).then(function() {
            grid.createGrid().then(function() {
                grid.w2ui.unlock();
            });

            grid.w2ui.lock('Loading parameters...', true);

            grid.on('change', function gridChange(event) {
                grid.w2ui.lock('Saving to Fusion 360...', true);
                grid.w2ui.status('Saving to Fusion 360');
                console.log('Grid Changed!');
                event.done(function(e) {
                    var record = grid.w2ui.records[e.index];
                    var field = grid.w2ui.columns[e.column].field;
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
                            grid.w2ui.unlock();
                            if (data.status === 'success') {
                                grid.w2ui.save();
                            } else {
                                record.w2ui.changes = {};
                                grid.w2ui.refresh();
                                grid.w2ui.error(
                                    'There was an error while trying to save changes to Fusion 360. <br> Error message: ' + data.message
                                );
                            }
                        }
                    );
                });
                console.log('Grid change done');
            });

            grid.on('editField', function gridEditField(event) {
                if (event.originalEvent.keyCode === 13) {
                    event.preventDefault();
                }
            });

            grid.on('dblClick', function(event) {
                console.log('dblClick');
            });
        });
    };

    return {
        init: init
    };
});
