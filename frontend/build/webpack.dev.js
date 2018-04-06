'use strict';

const webpack = require('webpack');
const path = require('path');
const notifier = require('node-notifier');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const FriendlyErrorsPlugin = require('friendly-errors-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const portfinder = require('portfinder');

const devWebpackConfig = {
  context: path.resolve(__dirname, '../'),
  entry: {
    cms: './src/cms.js',
    subscription: './src/subscription.js',
    participants: './src/participants.js',
    mg_attendee: './src/mg_attendee.js',
    mg_presence: './src/mg_presence.js',
    mg_swar: './src/mg_swar.js',
    mg_trn: './src/mg_trn.js',
    view_trn: './src/view_trn.js',
  },
  output: {
    path: path.resolve(__dirname, '../dist'),
    filename: '[name].js',
    publicPath: 'http://localhost:8080/static/'
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': path.join(__dirname, '..', 'src'),
    }
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
            css: [
              'vue-style-loader',
              { loader: 'css-loader', options:{ sourceMap:true}}
            ],
            scss: [
              'vue-style-loader',
              { loader: 'css-loader', options:{ sourceMap:true}},
              { loader: 'scss-loader',options:{ sourceMap:true}}
            ],
            stylus: [
              'vue-style-loader',
              { loader: 'css-loader', options:{ sourceMap:true}},
              { loader: 'stylus-loader',options:{ sourceMap:true}}
            ],
          },
          cssSourceMap: true,
          cacheBusting: true,
          transformToRequire: {
            video: ['src', 'poster'],
            source: 'src',
            img: 'src',
            image: 'xlink:href'
          }
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [
          path.join(__dirname, '../src'),
          path.join(__dirname, '../test'),
          path.join(__dirname, '../node_modules/webpack-dev-server/client')
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'static/img/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'static/media/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 10000,
          name: 'static/fonts/[name].[hash:7].[ext]'
        }
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          { loader: 'css-loader', options:{ sourceMap:true}}
        ]
      },
      { test: /\.postcss$/,
        use: [
          'vue-style-loader',
          { loader: 'css-loader', options:{ sourceMap:true}}
        ]
      },
      { test: /\.scss$/,
        use: [
          'vue-style-loader',
          { loader: 'css-loader', options:{ sourceMap:true}},
          { loader: 'sass-loader', options:{ sourceMap:true}}
        ]
      },
      { test: /\.styl$/,
        use: [
          'vue-style-loader',
          { loader: 'css-loader', options:{ sourceMap:true}},
          { loader: 'stylus-loader', options:{ sourceMap:true}}
        ]
      }
    ]
  },
  node: {
    setImmediate: false,
    dgram: 'empty',
    fs: 'empty',
    net: 'empty',
    tls: 'empty',
    child_process: 'empty'
  },
  devtool: 'cheap-module-eval-source-map',
  devServer: {
    clientLogLevel: 'warning',
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
    historyApiFallback: {
      rewrites: [
        { from: /.*/, to: path.posix.join('/', 'index.html') },
      ],
    },
    hot: true,
    contentBase: false, // since we use CopyWebpackPlugin.
    compress: true,
    host: 'localhost',
    port: 8080,
    open: true,
    overlay: {warnings: false, errors: true },
    publicPath: '/static/',
    proxy: {},
    quiet: true, // necessary for FriendlyErrorsPlugin
    watchOptions: {poll: false,}
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: '"development"'}
    }),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(), // HMR shows correct file names in console on update.
    new webpack.NoEmitOnErrorsPlugin(),
    new BundleTracker(
      {filename: './webpack-stats.json'}
    ),
    new CopyWebpackPlugin([
      {
        from: path.resolve(__dirname, '../static'),
        to: 'static',
        ignore: ['.*']
      }
    ])
  ]
};

module.exports = new Promise((resolve, reject) => {
  portfinder.basePort = 8080;
  portfinder.getPort((err, port) => {
    if (err) {
      reject(err)
    } else {
      devWebpackConfig.plugins.push(new FriendlyErrorsPlugin({
        compilationSuccessInfo: {
          messages: [`Your application is running: http://localhost:8080`],
        },
        onErrors: (severity, errors) => {
          if (severity !== 'error') return;
          const error = errors[0];
          const filename = error.file && error.file.split('!').pop();
          notifier.notify({
            title: 'bycco',
            message: severity + ': ' + error.name,
            subtitle: filename || '',
            icon: path.join(__dirname, 'logo.png')
          });
        }
      }));
      resolve(devWebpackConfig)
    }
  })
});
