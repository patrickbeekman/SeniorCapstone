/**
 * Created by patt on 2/20/18.
 */
module.exports = function(app) {
  var index = require('../controllers/index.server.controller.js');
  app.get('/helloworld', index.render);
};