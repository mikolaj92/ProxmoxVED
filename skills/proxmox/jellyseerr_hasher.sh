#!/usr/bin/env bash
set -euo pipefail
cd /app
node - <<'NODE'
let bcrypt;
try { bcrypt = require('bcryptjs'); }
catch(e) {
  try { bcrypt = require('bcrypt'); }
  catch(e2){ console.error('No bcrypt module'); process.exit(1); }
}
const pass = process.env.PASS || 'Test123';
(async()=>{
  if (bcrypt.hashSync) {
    console.log(bcrypt.hashSync(pass, 10));
  } else {
    const h = await bcrypt.hash(pass, 10);
    console.log(h);
  }
})();
NODE
