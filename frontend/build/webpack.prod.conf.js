'use strict';

const path = require('path');
const utils = require('./utils');
const webpack = require('webpack');
const config = require('../config/index');
const merge = require('webpack-merge');
const baseWebpackConfig = require('./webpack.base.conf');
const CopyWebpackPlugin = require('copy-webpack-plugin');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
// const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');

const webpackConfig = merge(baseWebpackConfig, {
  module: {
    rules: utils.styleLoaders({
      sourceMap: config.prod.productionSourceMap,
      extract: true
    })
  },
  devtool: config.prod.productionSourceMap ? '#source-map' : false,
  output: {
    path: path.resolve(config.prod.assetsRoot, config.prod.assetsSubDirectory),
    // filename: utils.assetsPath('js/[name].[chunkhash].js'),
    // chunkFilename: utils.assetsPath('js/[id].[chunkhash].js')
  },
  plugins: [

    new webpack.DefinePlugin({
      'process.env': config.prod.env
    }),

    // new webpack.optimize.UglifyJsPlugin({
    //   compress: {
    //     warnings: false
    //   },
    //   sourceMap: true
    // }),

    new ExtractTextPlugin({
      // filename: utils.assetsPath('css/[name].[contenthash].css')
      filename: 'css/[name].css'
    }),

    // new OptimizeCSSPlugin({
    //   cssProcessorOptions: {
    //     safe: true
    //   }
    // }),

    new CopyWebpackPlugin([
      {
        from: './static/img',
        to: path.resolve(config.prod.assetsRoot, config.prod.assetsSubDirectory, "img")
      }
    ])
  ]
});

// if (config.prod.productionGzip) {
//
//   const CompressionWebpackPlugin = require('compression-webpack-plugin');
//
//   webpackConfig.plugins.push(
//     new CompressionWebpackPlugin({
//       asset: '[path].gz[query]',
//       algorithm: 'gzip',
//       test: new RegExp(
//         '\\.(' +
//         config.prod.productionGzipExtensions.join('|') +
//         ')$'
//       ),
//       threshold: 10240,
//       minRatio: 0.8
//     })
//   )
// }
//
// if (config.prod.bundleAnalyzerReport) {
//   const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
//   webpackConfig.plugins.push(new BundleAnalyzerPlugin())
// }

module.exports = webpackConfig;
