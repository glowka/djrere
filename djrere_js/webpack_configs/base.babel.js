var webpack = require('webpack');
var path = require('path');

var baseDir = path.join(__dirname, '../', '../');

module.exports = {
  entry: {
    'frontpage': [path.join(baseDir, './djrere_js/frontpage/client')],
    'graphiql': [path.join(baseDir, './djrere_js/graphiql/client')]
  },

  output: {
    path: path.join(baseDir, 'public/static/bundles/'),
    filename: '[name]-[hash].js',
    // publicPath set in inheriting files
  },

  module: {
    loaders: [
      // JS
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel',
        include: path.join(baseDir, 'djrere_js'),
      }
    ]
  },

  resolve: {
    extensions: ['', '.js']
  },

  plugins: [
    new webpack.DefinePlugin({
      'process.env': { NODE_ENV: JSON.stringify(process.env.NODE_ENV) }
    }),

    new webpack.optimize.OccurenceOrderPlugin()
  ],

  cache: false,
  localConsts: {
    production: process.env.NODE_ENV === 'production',
    baseDir: baseDir
  }
};
