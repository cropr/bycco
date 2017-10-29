const path = require('path');
const webpack = require ('webpack');

module.exports = {
  entry: {
    bycco: "./index.js",
    subscription: "./subscription/index.js",
    tournament: "./tournament/index.js"
  },
  output: {
    path: path.resolve(__dirname, "../fe_dist/static/"),
    filename: "[name].bundle.js",
    sourceMapFilename: '[name].bundle.js.map'
  },
  watch: true,
  module: {
    rules: [
      {
        test:/\.css$/,
        use: ['file-loader?name=../static/views/[name].[ext]']
      },
      {
        test:/\.scss$/,
        use: ['file-loader?name=../static/css/[name].css', 'sass-loader']
      },
      {
        test: /\.html$/,
        use: ['file-loader?name=../static/views/[name].[ext]']
      },
      {
        test: /\.png$/,
        use: ['file-loader?name=../static/img/[name].[ext]']
      },
      {
        test: /\.jpeg$/,
        use: ['file-loader?name=../static/img/[name].[ext]']
      }

    ]
  },
  devtool: 'source-map',
  plugins: [
    new webpack.ProvidePlugin({
        $: "jquery",
        jQuery: "jquery"
    })
  ]
};