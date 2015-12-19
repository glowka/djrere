var path = require('path');
var express = require('express');
var webpack = require('webpack');
var config = require('./webpack.config.babel');

var server = express();
var compiler = webpack(config);

server.use(require('webpack-dev-middleware')(compiler, {
  noInfo: true,
  publicPath: config.output.publicPath
}));

server.use(require('webpack-hot-middleware')(compiler));

server.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, 'index.html'));
});

server.listen(8080, 'localhost', function(err) {
  if (err) {
    console.log(err);
    return;
  }

  console.log('Listening at http://localhost:8080');
});
