/**
 * Created by patt on 2/20/18.
 */
var express = require('express'),
    bodyParser     = require('body-parser'),
    methodOverride = require('method-override');

module.exports = function() {
    var app = express();

    // get all data/stuff of the body (POST) parameters
    // parse application/json
    app.use(bodyParser.json());

    // parse application/vnd.api+json as json
    app.use(bodyParser.json({ type: 'application/vnd.api+json' }));

    // parse application/x-www-form-urlencoded
    app.use(bodyParser.urlencoded({ extended: true }));

    // override with the X-HTTP-Method-Override header in the request. simulate DELETE/PUT
    app.use(methodOverride('X-HTTP-Method-Override'));

    require('../app/routes/index.server.routes.js')(app);
    return app;
};