require(['postal', './lib/cycle'], function requireDebugger(ps) {
    ps.addWireTap(function wireTap(data, envelope) {
        var message = (typeof envelope === String) ?
            envelope : JSON.stringify(JSON.decycle(envelope));
        console.log(message);
    });
});