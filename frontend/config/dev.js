'use strict';

const path = require('path');
const root = path.resolve(__dirname, '..');
const staticpath = 'static';
const portfinder = require('portfinder');
const BundleTracker = require('webpack-bundle-tracker');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');

const webpackconfig =  {
  entry: {
    cms: './src/cms.js',
    subscription: './src/subscription.js',
    participants: './src/participants.js',
    mg_attendee: './src/mg_attendee.js',
  },
  output: {
    path: path.resolve(root, staticpath),
    filename: '[name].js',
    publicPath: 'http://localhost:8080/static/'
  },
  devtool: '#cheap-module-eval-source-map',
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.resolve(root, 'src'),
    }
  },
  devServer: {
    clientLogLevel: 'warning',
    compress: true,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    host: '127.0.0.1',
    hot: true,
    port: 8080,
    open: true,
    overlay: {
      warnings: true,
      errors: true
    },
    publicPath: '/'+ staticpath + '/',
    quiet: true,
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: ['style-loaders', 'css-loaders', 'stylus-loaders'],
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
        include: [path.resolve(root, 'src')]
      },
      {
        test:  /\.css$/,
        use: ['style-loader', 'css-loader'],
        include: [path.resolve(root, 'src')]
      },
      {
        test:  /\.styl$/,
        use: ['style-loader', 'css-loader', 'stylus-loader'],
        include: [path.resolve(root, 'src')]
      }
    ]
  },
  plugins: [
    new BundleTracker(
      {filename: './webpack-stats.json'}
    ),
  ]
};

module.exports = new Promise((resolve, reject) => {
  portfinder.basePort = 8080;
  portfinder.getPort((err, port) => {
    if (err) {
      reject(err)
    } else {
      webpackconfig.devServer.port = port;
      webpackconfig.plugins.push(new FriendlyErrorsPlugin({
        compilationSuccessInfo: {
          messages: [`Your application is running here: http://${webpackconfig.devServer.host}:${port}`],
        },
        onErrors: (severity, errors) => {
          if (severity !== 'error') return;
          const error = errors[0];
          const filename = error.file && error.file.split('!').pop();
          notifier.notify({
            title: 'Bycco',
            message: severity + ': ' + error.name,
            subtitle: filename || ''
          })
        }
      }));
      resolve(webpackconfig)
    }
  })
})
