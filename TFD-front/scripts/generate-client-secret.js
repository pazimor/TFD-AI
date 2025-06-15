const fs = require('fs');
const path = require('path');

const secret = process.env.CLIENT_SECRET_JSON;
if (!secret) {
  console.error('CLIENT_SECRET_JSON environment variable is not set');
  process.exit(1);
}

let json;
try {
  json = JSON.parse(secret);
} catch (err) {
  console.error('CLIENT_SECRET_JSON is not valid JSON');
  process.exit(1);
}

const target = path.join(__dirname, '../src/env/client_secret.json');
fs.writeFileSync(target, JSON.stringify(json, null, 2));
console.log(`client_secret.json written to ${target}`);
