import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional
from utils.logger import get_logger

logger = get_logger("JenkinsManager")

class JenkinsManager:
    """
    Production-grade Jenkins CI/CD REST API Manager.
    Handles authentication, CSRF crumbs, job triggers, queue polling,
    build monitoring, and test result extraction.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        username: str = "Neel_Gagan",
        api_token: str = "11b2496fe69a1809702c0c9d475213d1c2",
        job_name: str = "AnanyaElectrical-Project-Python-BDD",
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.api_token = api_token
        self.job_name = job_name

    def _get_auth_headers(self) -> dict[str, str]:
        headers = {"User-Agent": "Ananya-Playwright-Automation-Client"}
        if self.username and self.api_token:
            auth_str = f"{self.username}:{self.api_token}"
            encoded = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
            headers["Authorization"] = f"Basic {encoded}"
        return headers

    def get_crumb(self) -> dict[str, str]:
        crumb_url = f"{self.base_url}/crumbIssuer/api/json"
        headers = self._get_auth_headers()
        req = urllib.request.Request(crumb_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                crumb_field = data.get("crumbRequestField", "Jenkins-Crumb")
                crumb_val = data.get("crumb", "")
                return {crumb_field: crumb_val}
        except Exception as e:
            logger.warning(f"Failed to fetch CSRF crumb: {e}")
            return {}

    def check_connection(self) -> tuple[bool, str]:
        headers = self._get_auth_headers()
        req = urllib.request.Request(f"{self.base_url}/api/json", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return True, "Connected to Jenkins successfully."
                return False, f"Unexpected response status: {resp.status}"
        except Exception as err:
            return False, f"Connection failed to {self.base_url}: {err}"

    def trigger_build(
        self,
        parameters: Optional[dict[str, Any]] = None,
    ) -> tuple[bool, str, Optional[str]]:
        is_connected, msg = self.check_connection()
        if not is_connected:
            return False, f"Cannot trigger build: {msg}", None

        headers = self._get_auth_headers()
        headers.update(self.get_crumb())

        if parameters:
            query = urllib.parse.urlencode(parameters)
            url = f"{self.base_url}/job/{urllib.parse.quote(self.job_name)}/buildWithParameters?{query}"
        else:
            url = f"{self.base_url}/job/{urllib.parse.quote(self.job_name)}/build"

        req = urllib.request.Request(url, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                queue_url = resp.headers.get("Location")
                return True, f"Build queued for '{self.job_name}'", queue_url
        except urllib.error.HTTPError as err:
            return False, f"HTTP Error {err.code}: {err.reason}", None
        except Exception as err:
            return False, f"Failed to trigger build: {err}", None

    def get_last_build_status(self) -> dict[str, Any]:
        headers = self._get_auth_headers()
        url = f"{self.base_url}/job/{urllib.parse.quote(self.job_name)}/lastBuild/api/json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}
