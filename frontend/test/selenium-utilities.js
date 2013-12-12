var fs = require("fs");

exports.modules = {
    saveScreenshot: function(ptor, filename) {
        return ptor.takeScreenshot().then(function(data) {
            fs.writeFile("./test/captures/" + filename, data.replace(/^data:image\/png;base64,/, ""), "base64",
                function(err) {
                    if (err) {
                        throw err;
                    }
                });
        });
    }
};