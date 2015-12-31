var baseConfig = require('./dev.babel');
var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

baseConfig.plugins.push(new BundleTracker({
  dirname: baseConfig.localConsts.baseDir,
  filename: './var/webpack_stats/frontpage.dev.json'
}));

console.log(path.join(baseConfig.localConsts.baseDir, './var/webpack_stats/frontpage.dev.json'));

baseConfig.entry.frontpage = path.join(baseConfig.localConsts.baseDir, './djrere_js/frontpage/client');

module.exports = baseConfig;
