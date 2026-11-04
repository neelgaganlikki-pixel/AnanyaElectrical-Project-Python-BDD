import os
import pytest
import datetime
from pytest_bdd import given
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from core.environment_manager import EnvironmentManager
from core.self_healing_engine import SelfHealingEngine
from pages.home_page import HomePage
from pages.navigation_page import NavigationPage
from pages.contact_page import ContactPage
from ai.failure_analysis import FailureAnalyzer
from utils.screenshots import take_screenshot

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment: 'dev' (default) or 'production'"
    )
    parser.addoption(
        "--browser_type",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--heal-mode",
        action="store",
        default="ASSISTED",
        help="Self-healing locator mode: STRICT, ASSISTED (default), or AUTO"
    )

@pytest.fixture(scope="session")
def env_manager(request) -> EnvironmentManager:
    env_name = request.config.getoption("--env")
    mgr = EnvironmentManager()
    mgr.set_environment(env_name)
    print(f"\n==========================================")
    print(f"ACTIVE TEST ENVIRONMENT: {mgr.env_name.upper()}")
    print(f"TARGET BASE URL:        {mgr.base_url}")
    print(f"==========================================\n")
    return mgr

@pytest.fixture(scope="session")
def base_url(env_manager) -> str:
    return env_manager.base_url

@pytest.fixture(scope="session")
def browser_type_name(request) -> str:
    return request.config.getoption("--browser_type")

@pytest.fixture(scope="session")
def heal_mode(request) -> str:
    return request.config.getoption("--heal-mode")

@pytest.fixture(scope="session")
def self_healing_engine(heal_mode) -> SelfHealingEngine:
    return SelfHealingEngine(mode=heal_mode)

@pytest.fixture(scope="session")
def playwright_instance():
    p = sync_playwright().start()
    yield p
    try:
        p.stop()
    except Exception:
        pass

@pytest.fixture(scope="session")
def browser_instance(playwright_instance, browser_type_name):
    b_type = getattr(playwright_instance, browser_type_name)
    launch_args = {
        "headless": True
    }
    if browser_type_name == "chromium":
        launch_args["args"] = ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]

    browser = b_type.launch(**launch_args)
    yield browser
    try:
        browser.close()
    except Exception:
        pass

@pytest.fixture(scope="function")
def browser_context(browser_instance):
    context = browser_instance.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True
    )
    yield context
    try:
        context.close()
    except Exception:
        pass

@pytest.fixture(scope="function")
def page(browser_context) -> Page:
    pg = browser_context.new_page()
    yield pg
    try:
        pg.close()
    except Exception:
        pass

@pytest.fixture(scope="function")
def home_page(page, self_healing_engine) -> HomePage:
    return HomePage(page, self_healing_engine)

@pytest.fixture(scope="function")
def nav_page(page, self_healing_engine) -> NavigationPage:
    return NavigationPage(page, self_healing_engine)

@pytest.fixture(scope="function")
def contact_page(page, self_healing_engine) -> ContactPage:
    return ContactPage(page, self_healing_engine)

# Shared BDD Steps
@given("I navigate to the Ananya Electrical Solutions homepage")
def navigate_homepage_common(page: Page, base_url: str):
    page.goto(base_url, wait_until="networkidle")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture:
            try:
                screenshot_path = take_screenshot(page_fixture, f"failure_{item.name}")
                analyzer = FailureAnalyzer()
                env_mgr = EnvironmentManager()
                analyzer.analyze_failure(
                    test_name=item.name,
                    environment=env_mgr.active_env,
                    base_url=env_mgr.base_url,
                    exception=call.excinfo.value if call.excinfo else Exception("Test Failure"),
                    screenshot_path=screenshot_path
                )
            except Exception as e:
                print(f"Error during failure hook processing: {e}")
