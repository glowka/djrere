var path = require('path');
var express = require('express');
var requestProxy = require('express-request-proxy');
var webpack = require('webpack');
var programInterface = require('commander');
var url = require('url');
var cors = require('cors');


// Load config

programInterface
  .option('-c, --config [filepath]', 'Set relative or absolute path to config', './djrere_js/webpack_configs/frontpage.dev.babel')
  .parse(process.argv);
var configPath = path.join(__dirname, programInterface.config);
console.log('Using config ', configPath);
var config = require(configPath);

// Init webpack and server

var expressApp = express();
var webpackCompiler = webpack(config);
var publicUrl = url.parse(config.output.publicPath);

if (publicUrl.href.indexOf('://') == -1 || !publicUrl.hostname)
  throw Error('output.publicPath setting from webpack config file should contain protocol and hostname.');


// Configure routing
expressApp.use(cors());
expressApp.use(require('webpack-dev-middleware')(webpackCompiler, {
  noInfo: true,
  publicPath: config.output.publicPath
}));
expressApp.use(require('webpack-hot-middleware')(webpackCompiler));
// All other handle by this server
expressApp.get('*', function(req, res) {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Listen

expressApp.listen(publicUrl.port, publicUrl.hostname, function(err) {
  if (err) {
    console.log(err);
    return;
  }
  console.log('Listening at ', publicUrl.host);
});