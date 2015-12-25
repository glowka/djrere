var webpack = require('webpack');
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

var production = process.env.NODE_ENV === 'production';
var host = 'http://localhost:3000';

module.exports = {
  entry: [
    './src/client',
    'webpack-hot-middleware/client?path=' + host + '/__webpack_hmr'
  ],
  output: {
    path: path.join(__dirname, 'public/static/bundles/'),
    filename: 'bundle.js',
    publicPath: host + '/static/bundles/'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel',
        include: path.join(__dirname, 'src'),
      },
      {
        test: /\.css$/,
        loader: 'style!css'
      }
    ]
  },
  resolve: {
    extensions: ['', '.js']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: JSON.stringify(process.env.NODE_ENV)}
    }),

    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),

    new BundleTracker({filename: './webpack-stats.json'}),

    (production ? new webpack.optimize.UglifyJsPlugin({
        compressor: {
          warnings: false
        }
    }) : function(){})
  ],
  devtool: production ? 'source-map' : 'eval-source-map',
  cache: false
};
