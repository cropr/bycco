'use strict';

const path = require('path');
const utils = require('../build/utils');
const webpack = require('webpack')
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const notifier = require('node-notifier');

const root = path.resolve(__dirname, '../../fe_dist');
const staticpath = 'static';

module.exports = {
  assetsRoot: root ,
  assetsSubDirectory: staticpath,
  proxyTable: {},
  webpackconfg: {
    entry: {
      cms: './src/cms.js',
      subscription: './src/subscription.js',
      participants: './src/participants.js',
      mg_attendee: './src/mg_attendee.js',
    },
    output: {
      path: path.resolve(root, staticpath),
      filename: '[name].js',
      publicPath: '/static/'
    },
    devtool: '#source-map',
    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
        '@': utils.resolve('src'),
      }
    },
    module: {
      rules: [{
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: utils.cssLoaders({
              sourceMap: true,
              minimize: true,
              extract: true
            }),
            transformToRequire: {
              video: 'src',
              source: 'src',
              img: 'src',
              image: 'xlink:href'
            }
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: [utils.resolve('src')]
        },
        // {
        //   test: /\.styl$/,
        //   use: ['style-loader', 'css-loader', 'stylus-loader']
        // }
        {
          test: /\.styl$/,
          use: ExtractTextPlugin.extract({
            fallback: "style-loader",
            use: ['css-loader','stylus-loader']
          })
        }
      ]
    },
    plugins: [
      new UglifyJsPlugin(),
      new webpack.optimize.CommonsChunkPlugin({
        name: 'vendor',
        minChunks (module) {
          // any required modules inside node_modules are extracted to vendor
          return (
            module.resource &&
            /\.js$/.test(module.resource) &&
            module.resource.indexOf(
              path.join(__dirname, '../node_modules')
            ) === 0
          )
        }
      }),
      new webpack.optimize.CommonsChunkPlugin({
        name: 'manifest',
        minChunks: Infinity
      }),
      new CopyWebpackPlugin([
        {
          from: './static',
          to: path.resolve(root, staticpath)
        },
        {
          from: './src/img',
          to: path.resolve(root, staticpath, "img")
        },
        {
          from: './node_modules/angular-material/angular-material.min.css',
          to: path.resolve(root, staticpath, "css", "angular-material.css")
        },
        {
          from: './node_modules/ui-cropper/compile/minified/ui-cropper.css',
          to: path.resolve(root, staticpath, "css", "ui-cropper.css")
        },
      ]),
      new ExtractTextPlugin("css/bycco.css"),
      new BundleTracker(
        {filename: './webpack-stats.json'}
      ),
      // new OptimizeCSSPlugin({
      //   cssProcessorOptions: { safe: true, map: { inline: false }}
      // }),
    ]
  }
};
