'use strict';

const path = require('path');
const utils = require('../build/utils');

const root = path.resolve(__dirname, '../../fe_dist');
const staticpath = 'static';

module.exports = {
  assetsRoot: root ,
  assetsSubDirectory: staticpath,
  assetsPublicPath: '/',
  productionGzip: false,
  productionGzipExtensions: ['js', 'css'],

  webpackconfg: {
    entry: {
      cms: './src/cms.js',
      subscription: './src/subscription.js',
      mg_attendee: './src/mg_attendee.js',
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
        }
      ]
    },
    devtool: config.productionSourceMap ,
    output: {
      path: path.resolve(root, staticpath)
    },
    plugins: [
      new CopyWebpackPlugin([
        {
          from: './src/img',
          to: path.resolve(root, staticpath, "img")
        },
        {
          from: './src/stylus/bycco.css',
          to: path.resolve(root, staticpath, "css", "bycco.css")
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
    ]
  }
};
