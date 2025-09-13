#!/usr/bin/env python3
import hashlib
import getpass

plain = getpass.getpass("Parola: ")
hashed = hashlib.sha256(plain.encode("utf-8")).hexdigest()
print(f"Hash SHA-256: {hashed}")
