define(['jquery', 'underscore', 'postal', './grid', 'text!../../css/grid.css'], function requireParametersGrid($, _, ps, Grid, css) {
    $('head').append('<style>' + css + '</style>');
    var config = {
        showSearchInColumns: true,
        name: 'parametersGrid',
        method: 'GET',
        recordHeight: 40,
        recid: 'ID',
        columns: [
            {
                field: 'ID',
                caption: 'ID',
                sortable: true,
                size: '25%',
            },
            {
                field: 'Group',
                caption: 'Group',
                sortable: true,
                size: '25%',
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'Name',
                caption: 'Name',
                sortable: true,
                size: '25%',
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'Expression',
                caption: 'Expression',
                size: 250,
                searchType: 'text',
                editable: { type: 'text' }
            },
            {
                field: 'Value',
                caption: 'Value',
                sortable: true,
                size: '25%'
            },
            {
                field: 'Unit',
                caption: 'Unit',
                size: 25,
                searchType: 'select'
            },
            {
                field: 'Comments',
                caption: 'Comments',
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
                event.done(function() {
                    console.log('Grid change done');
                });
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
