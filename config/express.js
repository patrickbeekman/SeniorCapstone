/**
 * Created by patt on 2/20/18.
 */
var express = require('express');

module.exports = function() {
  var app = express();
  require('../app/routes/index.server.routes.js')(app);
  return app;
};