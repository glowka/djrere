var baseConfig = require('./base.babel');
var webpack = require('webpack');
var path = require('path');


baseConfig.output.publicPath = '/static/bundles/';

baseConfig.plugins.push(
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  })
);

baseConfig.plugins.push(
  new BundleTracker({
    dirname: baseConfig.localConsts.baseDir,
    filename: './var/webpack_stats/prod.json'
  })
);


baseConfig.devtool = 'source-map';

module.exports = baseConfig;
