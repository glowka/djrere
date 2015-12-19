var HtmlWebpackPlugin = require('html-webpack-plugin'),
  webpack = require('webpack'),
  path = require('path');

var production = process.env.NODE_ENV === 'production';

module.exports = {
  entry: [
    './src/client',
    'webpack-hot-middleware/client'
  ],
  output: {
    path: path.join(__dirname, 'build'),
    filename: 'bundle.js',
    publicPath: '/assets/'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        loaders: ['babel'],
        include: path.join(__dirname, 'src')
      },
      {
        test: /\.css$/,
        loader: 'style!css'
      }
    ]
  },
  resolve: {
    //root: __dirname + '/node_modules',
    extensions: ['', '.js']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: JSON.stringify(process.env.NODE_ENV)}
    }),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin()
  ],
  devtool: production ? 'source-map' : 'eval-source-map',
  cache: false
};
