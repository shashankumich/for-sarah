#!/usr/bin/env python3
"""Seal site.src.html behind a passcode -> index.html (self-decrypting gate page).

usage: python3 build.py "passcode"
The passcode is normalised (lowercase, letters+digits only) on both sides.
"""
import base64, hashlib, os, re, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

if len(sys.argv) < 2:
    sys.exit("usage: build.py PASSCODE")
pw = re.sub(r"[^a-z0-9]", "", sys.argv[1].lower())
html = open("site.src.html", encoding="utf-8").read()
salt, iv = os.urandom(16), os.urandom(12)
key = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, 200_000, 32)
ct = AESGCM(key).encrypt(iv, html.encode("utf-8"), None)
b64 = lambda x: base64.b64encode(x).decode()
gate = open("gate.template.html", encoding="utf-8").read()
out = gate.replace("__SALT__", b64(salt)).replace("__IV__", b64(iv)).replace("__CT__", b64(ct))
open("index.html", "w", encoding="utf-8").write(out)
print(f"sealed {len(html)} bytes -> index.html ({len(out)} bytes), passcode normalised to {pw!r}")
