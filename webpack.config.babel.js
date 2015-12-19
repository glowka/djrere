import HtmlWebpackPlugin from 'html-webpack-plugin';
import webpack from 'webpack';
import path from 'path';

const production = process.env.NODE_ENV === 'production';

export default {
  entry: [
    './src/client',
    'webpack/hot/dev-server'
  ],
  output: {
    path: './build',
    filename: 'bundle.js',
    publicPath: '/'
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
    extensions: ['', '.js']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: JSON.stringify(process.env.NODE_ENV)}
    }),
    new HtmlWebpackPlugin({
      title: 'DjReRe'
    }),
  ],
  devtool: production ? 'source-map' : 'eval-source-map',
  devServer: {
    contentBase: './build'
  },
  cache: false
};
