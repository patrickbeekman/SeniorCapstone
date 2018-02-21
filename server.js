// server.js

// modules =================================================
var express        = require('./config/express.js');
var express2       = require('express');
var app            = express();
var mongoose	   = require('mongoose');

// configuration ===========================================

// config files
var db = require('./config/db');

// set our port
var port = process.env.PORT || 8080;

// connect to our mongoDB database
// (uncomment after you enter in your own credentials in config/db.js)
mongoose.connect(db.url);

// set the static files location /public/img will be /img for users
app.use(express2.static(__dirname + '/public'));

// routes ==================================================
require('./app/routes/routes')(app); // configure our routes

// start app ===============================================
// startup our app at http://localhost:8080
app.listen(port);

// shoutout to the user
console.log('Magic happens on port ' + port);

// expose app
exports = module.exports = app;
