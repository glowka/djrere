
module.exports = function (config) {
  config.set({
    browsers: ['Chrome'],
    singleRun: true,
    frameworks: ['mocha'],
    plugins: [
      'karma-webpack',
      'karma-sourcemap-loader',
      'karma-chrome-launcher',
      'karma-mocha',
      'karma-coverage',
      'karma-spec-reporter'
    ],
    files: [
      './djrere_js/**/*-test.js' // just load this file
    ],
    preprocessors: {
      './djrere_js/**/*-test.js': ['webpack', 'sourcemap']
    },
    reporters: ['spec', 'coverage'],
     coverageReporter: {
      dir: 'var/reports/coverage',
      reporters: [
        { type: 'html', subdir: 'report-html' },
        { type: 'lcov', subdir: 'report-lcov' },
        { type: 'cobertura', subdir: '.', file: 'cobertura.txt' }
      ]
    },
    webpack: {
      module: {
        loaders: [
          // JS
          { test: /\.jsx?$/,
            exclude: /node_modules/,
            loader: 'babel' },
          // CSS
          {
            test: /\.css$/,
            loader: 'style!css'
          },

          // LESS
          {
            test: /\.less$/,
            loader: 'style!css!less'
          }
        ],
        postLoaders: [{
          test: /\.jsx?$/, exclude: /(node_modules|(\-test\.jsx?$))/,
          loader: 'istanbul-instrumenter'
        }]
      },
      devtool: "inline-source-map"
    },
    webpackServer: {
      noInfo: true
    }
  });
};
