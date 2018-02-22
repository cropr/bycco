'use strict';

const path = require('path');
const utils = require('../build/utils');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");


const root = path.resolve(__dirname, '../../fe_dist');
const staticpath = 'static';

module.exports =  {
  assetsRoot: root ,
  assetsSubDirectory: staticpath,
  proxyTable: {},
  webpackconfig: {
    entry: {
      cms: './src/cms.js',
      subscription: './src/subscription.js',
      participants: './src/participants.js',
      mg_attendee: './src/mg_attendee.js',
    },
    output: {
      path: path.resolve(root, staticpath),
      filename: '[name].js',
      publicPath: '/'
    },
    devtool: '#cheap-module-eval-source-map',
    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
        '@': utils.resolve('src'),
      }
    },
    watch: true,
    module: {
      rules: [
        {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: utils.cssLoaders({
              sourceMap: false,
              minimize: false,
              extract: false
            }),
            transformToRequire: {
              video: 'src',
              source: 'src',
              img: 'src',
              image: 'xlink:href'
            }
          },
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          include: [utils.resolve('src')]
        },
        {
          test: /\.styl$/,
          use: ['style-loader', 'css-loader', 'stylus-loader']
          // use: ExtractTextPlugin.extract({
          //   use: ['style-loader', 'css-loader','stylus-loader']
          // })
        }
      ]
    },
    plugins: [
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
      new ExtractTextPlugin({
        filename: 'css/bycco.css',
        allChunks: true,
      })
    ],
  }
};
