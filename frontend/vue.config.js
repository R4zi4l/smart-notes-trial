if (process.env.NODE_ENV !== "development") {
  process.env.VUE_APP_WEBSOCKET_URL =
    "'wss://' + location.host + '/connection'";
  process.env.VUE_APP_SERVER_CONNECT_TIMEOUT = 10000;
  process.env.VUE_APP_SERVER_REQUEST_TIMEOUT = 60000;
} else {
  process.env.VUE_APP_WEBSOCKET_URL =
    "'ws://' + location.hostname + ':8000/connection'";
  process.env.VUE_APP_SERVER_CONNECT_TIMEOUT = 1000;
  process.env.VUE_APP_SERVER_REQUEST_TIMEOUT = 5000;
}

module.exports = {
  filenameHashing: process.env.NODE_ENV !== "development" ? false : true,

  publicPath: process.env.NODE_ENV !== "development" ? "/static/" : "/",

  outputDir: "../backend/static",

  css: {
    extract: true,
    sourceMap: true,
    loaderOptions: {
      sass: {
        prependData: `@import "@/styles/_variables.sass"`
      }
    }
  },

  chainWebpack: config => {
    config.plugins.delete("preload");
    config.plugins.delete("prefetch");

    if (process.env.NODE_ENV !== "development") {
      config.plugins.delete("html");
    }
  },

  devServer: {}
};
