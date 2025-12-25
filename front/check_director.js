const http = require('http');
const url = 'http://127.0.0.1:8000/api/content/director/';
http.get(url, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      console.log(JSON.stringify(json, null, 2));
    } catch (e) {
      console.error('Invalid JSON', e);
      console.log(data);
    }
  });
}).on('error', err => console.error('Error', err));

