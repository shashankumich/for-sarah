# For Sarah

A sealed birthday page. `index.html` is a passcode gate: the real page is AES-GCM-encrypted inside it
(key derived from the passcode with PBKDF2) and decrypted in the browser.

Rebuild after editing the source (`site.src.html`, not committed):

    python3 build.py "the passcode"
