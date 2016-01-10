var baseConfig = require('./base.babel');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var path = require('path');

// Specifying full host to load emulated static files from independent dev server
var host = 'http://localhost:3000';

baseConfig.entry.frontpage.push('webpack-hot-middleware/client?path=' + host + '/__webpack_hmr');

baseConfig.plugins.push(
  new webpack.HotModuleReplacementPlugin()
);

baseConfig.plugins.push(
  new BundleTracker({
    dirname: baseConfig.localConsts.baseDir,
    filename: './var/webpack_stats/dev.json'
  })
);

baseConfig.output.publicPath = host + '/static/bundles/';

baseConfig.devtool = 'eval-source-map';

module.exports = baseConfig;
