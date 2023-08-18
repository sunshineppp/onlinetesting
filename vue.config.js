const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/': {
        target: 'http://127.0.0.1:5000',
        ws: false
      }
    }
  },
  pages: {
    index: {
      entry: 'src/main.js',
      title: 'onlinetesting'
    }
  }
})