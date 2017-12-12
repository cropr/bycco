'use strict';

const path = require('path');
const utils = require('./utils');
const webpack = require('webpack');
const config = require('../config/index');
const merge = require('webpack-merge');
const baseWebpackConfig = require('./webpack.base.conf');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');


module.exports = merge(baseWebpackConfig, {
  // cheap-module-eval-source-map is faster for development
  devtool: '#cheap-module-eval-source-map',
  output: {
    path: path.resolve(config.cms.assetsRoot,config.cms.assetsSubDirectory)
  },
  watch: true,
  plugins: [
    new webpack.DefinePlugin({
      'process.env': config.cms.env
    }),
    new CopyWebpackPlugin([
      {
        from: './src/img',
        to: path.resolve(config.cms.assetsRoot, config.cms.assetsSubDirectory, "img")
      },
      {
        from: './src/stylus/bycco.css',
        to: path.resolve(config.cms.assetsRoot, config.cms.assetsSubDirectory,
          "css", "bycco.css")
      },
      {
        from: './node_modules/angular-material/angular-material.min.css',
        to: path.resolve(config.cms.assetsRoot, config.cms.assetsSubDirectory,
          "css", "angular-material.css")
      },
      {
        from: './node_modules/ui-cropper/compile/minified/ui-cropper.css',
        to: path.resolve(config.cms.assetsRoot, config.cms.assetsSubDirectory,
          "css", "ui-cropper.css")
      },
    ])
  ]
});
