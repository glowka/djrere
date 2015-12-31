var baseConfig = require('./base.babel');
var webpack = require('webpack');


baseConfig.entry.dev = 'webpack-hot-middleware/client?path=' + baseConfig.localConsts.host + '/__webpack_hmr';

baseConfig.plugins.push(
  new webpack.HotModuleReplacementPlugin()
);

baseConfig.devtool = 'eval-source-map';

module.exports = baseConfig;
