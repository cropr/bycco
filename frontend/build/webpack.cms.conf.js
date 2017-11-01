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
  module: {
    rules: utils.styleLoaders({
      sourceMap: config.dev.cssSourceMap,
      extract: true
    })
  },
  // cheap-module-eval-source-map is faster for development
  devtool: '#cheap-module-eval-source-map',
  output: {
    path: path.resolve(config.cms.assetsRoot,config.cms.assetsSubDirectory)
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': config.cms.env
    }),
    new ExtractTextPlugin({
      filename: 'css/[name].css'
    }),
    new CopyWebpackPlugin([
      {
        from: './static/img',
        to: path.resolve(config.cms.assetsRoot, config.cms.assetsSubDirectory, "img")
      },
    ])
  ]
});
