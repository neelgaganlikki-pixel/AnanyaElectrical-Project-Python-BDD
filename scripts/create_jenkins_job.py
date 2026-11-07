import urllib.request
import urllib.parse
import urllib.error
import base64
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

JENKINS_URL = "http://localhost:8080"
USER = "Neel_Gagan"
TOKEN = "11b2496fe69a1809702c0c9d475213d1c2"
JOB_NAME = "AnanyaElectrical-Project-Python-BDD"
REPO_URL = "https://github.com/neelgaganlikki-pixel/AnanyaElectrical-Project-Python-BDD.git"

auth_header = "Basic " + base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()

# 1. Fetch Crumb
crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
req = urllib.request.Request(crumb_url, headers={"Authorization": auth_header})
headers = {
    "Authorization": auth_header,
    "Content-Type": "application/xml"
}

try:
    with urllib.request.urlopen(req) as resp:
        crumb_data = json.loads(resp.read().decode())
        crumb_field = crumb_data.get("crumbRequestField", "Jenkins-Crumb")
        crumb_value = crumb_data.get("crumb")
        headers[crumb_field] = crumb_value
        print(f"Acquired CSRF Crumb: {crumb_field}")
except Exception as e:
    print(f"Warning: Could not fetch crumb ({e}), proceeding without it")

job_xml = f"""<?xml version="1.1" encoding="UTF-8"?>
<flow-definition plugin="workflow-job">
  <actions>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition"/>
  </actions>
  <description>Enterprise AI-Powered Playwright Python Automation Framework for Ananya Electrical Solutions with Self-Healing Locators, Page Object Model, and Pytest-BDD.</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
      <triggers>
        <com.cloudbees.jenkins.GitHubPushTrigger plugin="github">
          <spec></spec>
        </com.cloudbees.jenkins.GitHubPushTrigger>
        <hudson.triggers.SCMTrigger>
          <spec>H/2 * * * *</spec>
          <ignorePostCommitHooks>false</ignorePostCommitHooks>
        </hudson.triggers.SCMTrigger>
      </triggers>
    </org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
    <scm class="hudson.plugins.git.GitSCM" plugin="git">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>{REPO_URL}</url>
          <credentialsId>gmail-jenkins</credentialsId>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/main</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="empty-list"/>
      <extensions/>
    </scm>
    <scriptPath>Jenkinsfile</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
"""

# Check if job already exists
check_url = f"{JENKINS_URL}/job/{urllib.parse.quote(JOB_NAME)}/api/json"
check_req = urllib.request.Request(check_url, headers={"Authorization": auth_header})
job_exists = False
try:
    with urllib.request.urlopen(check_req) as resp:
        if resp.status == 200:
            job_exists = True
except urllib.error.HTTPError as e:
    if e.code == 404:
        job_exists = False

if job_exists:
    print(f"Job '{JOB_NAME}' already exists. Updating configuration...")
    update_url = f"{JENKINS_URL}/job/{urllib.parse.quote(JOB_NAME)}/config.xml"
    req = urllib.request.Request(update_url, data=job_xml.encode('utf-8'), headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(f"Job updated successfully: HTTP {resp.status}")
else:
    print(f"Creating new Jenkins Pipeline Job: '{JOB_NAME}'...")
    create_url = f"{JENKINS_URL}/createItem?name={urllib.parse.quote(JOB_NAME)}"
    req = urllib.request.Request(create_url, data=job_xml.encode('utf-8'), headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(f"Job created successfully: HTTP {resp.status}")

# Verify job details
req = urllib.request.Request(check_url, headers={"Authorization": auth_header})
with urllib.request.urlopen(req) as resp:
    info = json.loads(resp.read().decode())
    print("\nVerified Jenkins Job in System:")
    print(f"  Name:        {info.get('name')}")
    print(f"  URL:         {info.get('url')}")
    print(f"  Buildable:   {info.get('buildable')}")
    print(f"  Color:       {info.get('color')}")

