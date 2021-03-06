var webpack = require('webpack');
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
var path = require('path');

var baseDir = path.join(__dirname, '../', '../');

module.exports = {
  entry: {
    'frontpage': [path.join(baseDir, './djrere_js/frontpage/client')],
    'blog': [path.join(baseDir, './djrere_js/blog/client')],
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
        // Load using babel only own modules
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

    new webpack.optimize.OccurenceOrderPlugin(),

    new CommonsChunkPlugin('commons', "commons-[hash].js")
  ],

  cache: false,
  localConsts: {
    production: process.env.NODE_ENV === 'production',
    baseDir: baseDir
  }
};
