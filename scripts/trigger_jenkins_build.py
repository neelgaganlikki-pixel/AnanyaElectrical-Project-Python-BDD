import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

JENKINS_URL = "http://localhost:8080"
USER = "Neel_Gagan"
TOKEN = "11b2496fe69a1809702c0c9d475213d1c2"
JOB_NAME = "AnanyaElectrical-Project-Python-BDD"

auth_header = "Basic " + base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()

# 1. Fetch Crumb
crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
req = urllib.request.Request(crumb_url, headers={"Authorization": auth_header})
headers = {
    "Authorization": auth_header
}

try:
    with urllib.request.urlopen(req) as resp:
        crumb_data = json.loads(resp.read().decode())
        crumb_field = crumb_data.get("crumbRequestField", "Jenkins-Crumb")
        crumb_value = crumb_data.get("crumb")
        headers[crumb_field] = crumb_value
except Exception as e:
    pass

# Trigger build with parameters
params = {
    "TARGET_ENVIRONMENT": "dev",
    "BROWSER_TYPE": "chromium",
    "SELF_HEALING_MODE": "ASSISTED",
    "PYTEST_MARKER": "smoke"
}
query_str = urllib.parse.urlencode(params)
build_url = f"{JENKINS_URL}/job/{urllib.parse.quote(JOB_NAME)}/buildWithParameters?{query_str}"
print(f"Triggering build on {build_url}...")
req = urllib.request.Request(build_url, headers=headers, method="POST")

with urllib.request.urlopen(req) as resp:
    queue_url = resp.headers.get("Location")
    print(f"Build queued successfully! HTTP {resp.status}")
    print(f"Queue item: {queue_url}")

# Poll queue until build starts
build_number = None
if queue_url:
    print("Waiting for build to start in queue...")
    for _ in range(15):
        time.sleep(2)
        q_req = urllib.request.Request(f"{queue_url}api/json", headers=headers)
        try:
            with urllib.request.urlopen(q_req) as q_resp:
                q_data = json.loads(q_resp.read().decode())
                if "executable" in q_data and q_data["executable"]:
                    build_number = q_data["executable"].get("number")
                    print(f"Build started! Build Number: #{build_number}")
                    break
        except Exception:
            break

print(f"\nJenkins Build URL: {JENKINS_URL}/job/{JOB_NAME}/{build_number or ''}")
