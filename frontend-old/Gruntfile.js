'use strict';

const webpackConfig = require('./webpack.config');
const path = require('path');

module.exports = function (grunt) {

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // load tasks
  grunt.loadNpmTasks('grunt-webpack');

  // Define the configuration for all the tasks
  grunt.initConfig({
    webpack: {
      dev: webpackConfig
    },

    maildev: {
      run: {
        keepAlive: true,
        open: true
      }
    },

    "webpack-dev-server": {
      options: {
        webpack: webpackConfig,
      },
      start: {
        contentBase: path.join(__dirname, "dist"),
        compress: true,
        port: 9000
      }
    }
  })

};
