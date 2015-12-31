var baseConfig = require('./prod.babel');
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');


baseConfig.plugins.push(new BundleTracker({
  dirname: baseConfig.localConsts.baseDir,
  filename: './var/webpack_stats/frontpage.prod.json'
}));


baseConfig.entry.frontpage = path.join(baseConfig.localConsts.baseDir, './djrere_js/frontpage/client');

module.exports = baseConfig;
