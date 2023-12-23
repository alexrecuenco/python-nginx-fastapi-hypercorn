#!/usr/bin/env node
// Just for debugging
// See https://gist.github.com/bszwej/62c327d773051816ed4949fd40c82c74

const http = require("http");
const server = http.createServer();

console.log("Starting server...");
server
  .on("request", (request, response) => {
    console.log("> Request received\n---\n");
    let body = [];
    request
      .on("data", (chunk) => {
        body.push(chunk);
      })
      .on("end", () => {
        body = Buffer.concat(body).toString();

        console.log(`==== ${request.method} ${request.url}`);
        console.log("> Headers");
        console.log(request.headers);

        console.log("> Body");
        console.log(body ?? "> NO BODY <");
        response.end();
      });
  })
  .listen(8000)
  .on("listening", () => console.log("Listening"));
