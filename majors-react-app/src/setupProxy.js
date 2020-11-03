const {createProxyMiddleware} = require('http-proxy-middleware');
const proxy = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(createProxyMiddleware('/api/', { 
      target: 'http://3.231.174.85:5000'
    }));
  }
