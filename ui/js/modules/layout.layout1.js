define(['jquery', 'underscore', 'postal', './layout'], function requireLayout1($, _, ps, Layout) {
    var PSTYLE = 'border: 1px solid #dfdfdf; padding: 5px;';
    var config =
        {
            name: 'layout1',
            selector: '#layout1',
            panels: [
                { type: 'left', size: 200, hidden: true, resizable: true, content: 'left', style: PSTYLE },
                { type: 'preview', size: 400, hidden: false, resizable: true, content: 'preview', style: PSTYLE },
                { type: 'main', content: 'main', overflow: 'none', style: PSTYLE }
            ]
        };
    var layout = new Layout('layout1', '#layout1', config);

    var init = function init() {
        $(function createLayout() {
            layout.createLayout();
            layout.on('resize');

            // layout.w2ui.hide('preview');

            // setTimeout(function() {
            //     layout.w2ui.show('preview');
            // }, 2000);

            layout.w2ui.content('preview', '<div id="messages"></div>');
            ps.subscribe({
                channel: 'layout',
                topic: 'layout1.preview',
                callback: function layout1PreviewOperation(data, envelope) {
                    layout.w2ui.content('preview', JSON.stringify(data, null, 4));
                }
            });
        });
    };

    return {
        init: init
    };
});