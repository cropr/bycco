'use strict';

const rm = require('rimraf');
const path = require('path');
const chalk = require('chalk');
const webpack = require('webpack');
const config = require('../config/prod');

console.log('building prod version');

rm(path.join(config.assetsRoot, config.assetsSubDirectory), err => {
  if (err) throw err;
  webpack(config.webpackconfg, function (err, stats) {
    if (err) throw err;
    process.stdout.write(stats.toString({
      colors: true,
      modules: false,
      children: false,
      chunks: false,
      chunkModules: false
    }) + '\n');

    if (stats.hasErrors()) {
      console.log(chalk.red('  Build failed with errors.\n'));
      process.exit(1)
    }

    console.log(chalk.cyan('  Build complete. + new Date()'));

  })
});
