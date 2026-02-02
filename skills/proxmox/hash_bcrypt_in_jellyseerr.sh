#!/usr/bin/env bash
set -euo pipefail
PASS="Test123"
docker exec jellyseerr node - <<'NODE'
const bcrypt = require('bcryptjs');
const pass = process.env.PASS;
console.log(bcrypt.hashSync(pass, 10));
NODE
