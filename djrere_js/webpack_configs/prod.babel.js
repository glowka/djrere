var baseConfig = require('./base.babel');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require('path');


baseConfig.module.loaders.push(
  // CSS
  {
    test: /\.css$/,
    loader: ExtractTextPlugin.extract("style-loader", "css-loader")
  },

  // LESS
  {
    test: /\.less$/,
    loader: ExtractTextPlugin.extract("style-loader", "css-loader!less-loader")
  }
);


baseConfig.plugins.push(
  new webpack.optimize.UglifyJsPlugin({
    compressor: {
      warnings: false
    }
  }),

  new BundleTracker({
    dirname: baseConfig.localConsts.baseDir,
    filename: './var/webpack_stats/prod.json'
  }),

  new ExtractTextPlugin("[name]-[hash].css")
);

baseConfig.output.publicPath = '/static/bundles/';

baseConfig.devtool = 'source-map';

module.exports = baseConfig;
