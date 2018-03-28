'use strict';

const rm = require('rimraf');
const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');
const root = path.resolve(__dirname, '../../static');
const staticpath = 'static';

const prodWebpackConfig = {
  entry: {
    cms: './src/cms.js',
    subscription: './src/subscription.js',
    participants: './src/participants.js',
    mg_attendee: './src/mg_attendee.js',
  },
  output: {
    path: root,
    filename: '[name]-[hash].js',
    publicPath: '/static/'
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
        use: ExtractTextPlugin.extract({
          fallback: "css-loader",
          use: ['css-loader']
        })
      },
      {
        test: /\.styl$/,
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: ['css-loader','stylus-loader']
        })
      },
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
  devtool: '#source-map',
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
    new webpack.DefinePlugin({
      'process.env': {NODE_ENV: '"production"'}
    }),
    new CopyWebpackPlugin([
      {
        from: './static',
        to: root
      },
    ]),
    new ExtractTextPlugin("css/bycco.css"),
    new BundleTracker(
      {filename: './webpack-stats.json'}
    ),
  ]
};

rm(path.resolve(root,staticpath ), err => {
  if (err) throw err;
  webpack(prodWebpackConfig, function (err, stats) {
    if (err) throw err;
    process.stdout.write(stats.toString({
      colors: true,
      modules: false,
      children: false,
      chunks: true,
      chunkModules: false
    }) + '\n');

    if (stats.hasErrors()) {
      console.log('  Build failed with errors.\n');
      process.exit(1)
    }
    console.log('  Build complete. + new Date()');

  })
});
