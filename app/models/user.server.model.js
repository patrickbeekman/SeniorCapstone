/**
 * Created by patt on 2/15/18.
 */

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;

var UserSchema = new Schema({
  id: String,
  name: String,
  gender: String,
  english: Number,
  maths: Number
});

mongoose.model('User', UserSchema);