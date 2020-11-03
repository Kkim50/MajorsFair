const {createProxyMiddleware} = require('http-proxy-middleware');
const proxy = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(createProxyMiddleware('/api/', { 
      target: 'https://majors-fair.herokuapp.com/'
    }));
  }
