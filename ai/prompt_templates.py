FAILURE_ANALYSIS_PROMPT = """
You are a Principal QA Automation Architect and AI Testing Engineer.
Analyze the following Playwright test failure on the Ananya Electrical Solutions website.

Test Details:
- Test Name: {test_name}
- Environment: {environment} ({base_url})
- Exception Type: {exception_type}
- Exception Message: {exception_message}
- Locator Attempted: {locator}
- Browser Console Errors: {console_errors}
- Failed Network Requests: {network_errors}

DOM Context:
{dom_snippet}

Please produce a structured diagnostic JSON response:
{{
  "category": "<Application defect | Locator issue | Timing issue | Network issue | Test data issue | Environment issue | Browser issue | Framework issue>",
  "root_cause_summary": "<concise explanation>",
  "impact_severity": "<Critical | Major | Minor | Low>",
  "suggested_fix": "<actionable recommendation for test engineer or developer>",
  "is_application_defect": <true | false>,
  "healing_recommended": <true | false>
}}
"""

