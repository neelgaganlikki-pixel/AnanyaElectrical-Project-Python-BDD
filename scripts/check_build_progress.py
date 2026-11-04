import urllib.request
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

JENKINS_URL = "http://localhost:8080"
USER = "Neel_Gagan"
TOKEN = "11b2496fe69a1809702c0c9d475213d1c2"
JOB_NAME = "AnanyaElectrical-Project-Python-BDD"
BUILD_NUM = 2

auth_header = "Basic " + base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()
url = f"{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUM}/consoleText"

req = urllib.request.Request(url, headers={"Authorization": auth_header})
try:
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode('utf-8')
        print(f"=== CONSOLE TEXT FOR BUILD #{BUILD_NUM} LAST 40 LINES ===")
        lines = text.strip().split('\n')
        for line in lines[-40:]:
            print(line)
except Exception as e:
    print(f"Error reading console: {e}")
