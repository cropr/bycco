'use strict';

const path = require('path');
const rm = require('rimraf');
const chalk = require('chalk');
const webpack = require('webpack');
const config = require('../config/dev');

console.log('building dev version');

rm(path.join(config.assetsRoot, config.assetsSubDirectory), err => {
  if (err) throw err;
  webpack(config.webpackconfig, function (err, stats) {
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

    console.log(chalk.cyan('  Build complete. ' + new Date() ));

  })
});
