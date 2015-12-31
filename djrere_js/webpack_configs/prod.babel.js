var baseConfig = require('./base.babel');
var webpack = require('webpack');
var path = require('path');


baseConfig.plugins.push(
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
);

baseConfig.devtool = 'source-map';

module.exports = baseConfig;
