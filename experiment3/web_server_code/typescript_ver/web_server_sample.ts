// run by bun run ./web_server_sample

import http from 'http'
import fs from 'fs'

const server = http.createServer((req, res) => {
  // fetch the request url
  const url = req.url
  
  fs.readFile(`../${url}.html`, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/html' })
      res.end(fs.readFileSync('../404.html'))
      return
    }
    
    res.writeHead(200, { 'Content-Type': 'text/html' })
    res.end(data)
  })
})

server.listen(3000, () => {
  console.log('server is listenning on port 3000')
})