define(['./modules/layout.layout1', './modules/grid.parameters', './modules/fusion'], function requireApp(layout1, gridParameters, fusion) {
    var init = function init() {
        fusion.init();
        gridParameters.init();
        layout1.init();
    };

    return {
        init: init
    };
});