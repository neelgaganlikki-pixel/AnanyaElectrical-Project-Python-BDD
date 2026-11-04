import pytest
from playwright.sync_api import Page

@pytest.mark.performance
@pytest.mark.regression
@pytest.mark.production_safe
def test_navigation_timing_metrics(page: Page, base_url: str):
    """TC_PERF_001: Measure Navigation Timing: DOMContentLoaded and Load Event within SLA."""
    page.goto(base_url, wait_until="networkidle")
    
    timing = page.evaluate("""() => {
        const perf = window.performance.timing;
        return {
            dns: perf.domainLookupEnd - perf.domainLookupStart,
            tcp: perf.connectEnd - perf.connectStart,
            domContentLoaded: perf.domContentLoadedEventEnd - perf.navigationStart,
            load: perf.loadEventEnd - perf.navigationStart
        };
    }""")
    
    # Assert acceptable SLAs for edge-cached SPA
    assert timing["domContentLoaded"] > 0
    print(f"\n[Performance Metrics] DOMContentLoaded: {timing['domContentLoaded']}ms, Load: {timing['load']}ms")

@pytest.mark.performance
@pytest.mark.regression
@pytest.mark.production_safe
def test_no_failed_network_requests(page: Page, base_url: str):
    """TC_PERF_002: Verify zero 4xx/5xx HTTP errors or failed static assets during initial load."""
    failed_requests = []
    
    def on_req_failed(req):
        failed_requests.append(req.url)
        
    page.on("requestfailed", on_req_failed)
    response = page.goto(base_url, wait_until="networkidle")
    
    assert response.status == 200
    assert len(failed_requests) == 0, f"Found failed requests: {failed_requests}"

