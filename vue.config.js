const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');

// https://cli.vuejs.org/config/
module.exports = {
  outputDir: 'static/bundles',
  publicPath: 'static/bundles',
  lintOnSave: process.env.NODE_ENV !== 'production',
  chainWebpack: config => {
    config.optimization.delete('splitChunks')
  },
  css: {
    extract: false
  },
  configureWebpack: config => {

    // Remove the default entry point
    delete config.entry.app;

    return {
      entry: {
        global: './static/js/global',
        compose: './static/js/compose',
        requestgroup_detail: './static/js/requestgroup_detail',
        request_detail: './static/js/request_detail',
        telescope_availability_chart: './static/js/telescope_availability_chart',
        paginate_dropdown: './static/js/components/util/paginate_dropdown',
        tools: './static/js/tools'
      },
      output: {
        filename: process.env.NODE_ENV === 'production'
          ? '[name].[contenthash].js'
          : '[name].[hash].dev.js'
      },
      plugins: [
        new BundleTracker({filename: './static/webpack-stats.json'}),
        new webpack.HashedModuleIdsPlugin()
      ],
      optimization: {
        splitChunks: {
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendor',
              chunks: 'all'
            }
          }
        }
      },
      resolve: {
        alias: {
          // This is needed for jquery-file-download/src/Scripts/jquery.fileDownload.js to work
          'jquery': path.join(__dirname, 'node_modules/jquery/src/jquery'),
          'bootstrap-components': path.resolve(__dirname, 'node_modules/bootstrap-vue/es/components')
        }
      }
    };
  }
}
