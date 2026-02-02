#!/usr/bin/env python3
import bcrypt
import sys

password = b'arradmin123'
hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
print(hashed.decode())
