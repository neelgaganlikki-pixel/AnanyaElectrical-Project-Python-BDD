# Ananya Electrical Solutions - AI-Powered Playwright Python Automation Framework

Enterprise-grade test automation framework engineered with **Python**, **Playwright**, **Pytest**, **Pytest-BDD**, **Page Object Model (POM)**, and an intelligent **AI-Assisted Self-Healing Locator Engine**.

Developed specifically for the **Ananya Electrical Solutions** web application, supporting multi-environment execution across Cloudflare Workers Development (`DEV`) and Production.

---

## 🏛️ Framework Architectural Highlights

- **Multi-Environment Orchestration:** Native support for `--env dev` (default) and `--env production` with built-in Safety Guards preventing destructive actions on production.
- **Controlled Self-Healing Engine:** Discovers, scores, and validates candidate locators when DOM shifts occur, without hiding actual application defects or accepting ambiguous selectors.
  - Modes: `STRICT` (no healing), `ASSISTED` (suggests candidates, captures audit trail), and `AUTO` (safely auto-heals high-confidence unique candidates).
- **AI-Assisted Failure Analysis:** Deterministic heuristic AI combined with LLM integration to automatically diagnose test failures, classify root causes (Application Defect, Locator, Timing, Network, Environment), and suggest corrective actions.
- **Enterprise Reporting:** Automated generation of HTML test reports, comprehensive Excel test inventories (`test_scenarios.xlsx`), self-healing dashboards, and Jira-ready defect dossiers.
- **Jenkins CI/CD Pipeline:** Declarative multi-stage Jenkins pipeline with parameterization, environment safety checks, artifact archiving, and automated report publishing.

---

## 📂 Project Directory Structure

```
Ananya_Automation/
├── config/
│   └── config.yaml                 # Multi-environment & framework configuration
├── core/
│   ├── browser_manager.py          # Playwright browser lifecycle manager
│   ├── driver_factory.py           # Driver instantiation factory
│   ├── environment_manager.py      # Environment switching & safety guard enforcement
│   ├── healing_history.py          # Self-healing persistent audit trail
│   ├── locator_engine.py           # Baseline locators & element fingerprint registry
│   ├── locator_validator.py        # Strict uniqueness & identity validation
│   └── self_healing_engine.py      # Core self-healing algorithm & scoring matrix
├── pages/
│   ├── base_page.py                # Base Page Object with self-healing hooks
│   ├── home_page.py                # Homepage POM implementation
│   ├── navigation_page.py          # Header, dropdowns, and modal catalogs POM
│   └── contact_page.py             # Consultation quote form POM
├── tests/
│   ├── test_functional.py          # Homepage loading, navigation, and modal tests
│   ├── test_negative.py            # Form validation, boundary values, and negative paths
│   ├── test_responsive.py          # Viewport reflow across desktop, tablet, and mobile
│   ├── test_integration.py         # WhatsApp, phone dialers, mailto, and Google Maps
│   ├── test_security.py            # HTTPS enforcement, tabnabbing prevention, XSS
│   ├── test_performance.py         # Navigation Timing & static asset health
│   ├── test_seo.py                 # SEO metadata, Open Graph, and JSON-LD structured data
│   ├── test_accessibility.py       # Form labels, button accessibility, image alt text
│   └── test_self_healing.py        # Controlled recovery & defect rejection verification
├── features/
│   ├── homepage.feature            # Gherkin BDD scenarios for homepage
│   ├── navigation.feature          # Gherkin BDD scenarios for header navigation & modal hub
│   └── contact.feature             # Gherkin BDD scenarios for quote form
├── step_definitions/
│   ├── test_homepage_steps.py      # Pytest-BDD step definitions for homepage
│   ├── test_navigation_steps.py    # Pytest-BDD step definitions for header navigation & modal hub
│   └── test_contact_steps.py       # Pytest-BDD step definitions for quote form
├── utils/
│   ├── dom_analyzer.py             # Deep DOM exploration utility
│   ├── failure_analyzer.py         # Defect triage & analysis
│   ├── jira_integration.py        # Jira REST API client & defect dossier generator
│   ├── logger.py                   # Centralized logging
│   ├── reporting.py                # Master execution summary generator
│   ├── screenshots.py              # Full-page screenshot capture
│   └── test_data.py                # Test fixture & data loader
├── ai/
│   ├── ai_client.py                # Dual heuristic & LLM diagnostic engine
│   ├── failure_analysis.py         # AI-powered test failure analysis
│   ├── locator_suggestions.py      # Suggests alternative locators
│   └── prompt_templates.py         # AI analysis prompt templates
├── test_data/
│   ├── test_data.json              # Structured test inputs and viewport matrix
│   └── test_scenarios.xlsx         # 39-scenario Excel test inventory
├── locators/
│   ├── baseline_locators.json      # Discovered element baselines
│   ├── healing_history.json        # Recovery action logs
│   └── healing_audit.json          # Metrics summary dashboard
├── reports/
│   ├── dom_analysis/               # DOM analysis report & captured HTML/PNGs
│   ├── html/                       # Pytest HTML execution reports
│   ├── screenshots/                # Failure & visual evidence screenshots
│   └── defects/                    # Automated defect dossiers
├── conftest.py                     # Custom pytest options, fixtures & failure hooks
├── pytest.ini                      # Pytest markers and configuration
├── Jenkinsfile                     # Declarative CI/CD pipeline
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

---

## 🚀 Quick Start & Execution Commands

### 1. Execute All Tests on DEV (Default Environment)
```bash
pytest --env dev
```

### 2. Execute Smoke Tests
```bash
pytest -m smoke --env dev
```

### 3. Execute Functional & Negative Validation
```bash
pytest -m "functional or negative" --env dev
```

### 4. Execute with HTML Report Generation
```bash
pytest --env dev --html=reports/html/report.html --self-contained-html
```

### 5. Execute Cross-Browser Tests
```bash
pytest -m functional --browser_type firefox
pytest -m functional --browser_type webkit
```

### 6. Execute Production Smoke Tests (Non-Destructive)
```bash
pytest -m smoke --env production
```

### 7. Execute Self-Healing Engine Verification
```bash
pytest -m healing
```

---

## 🛡️ Safety Guards & Production Rules
The framework enforces strict environment safeguards:
1. `DEV` is always the default environment.
2. Form submission on production is prevented unless explicitly approved.
3. Destructive actions on production throw `PermissionError` immediately.
4. The Self-Healing Engine never modifies permanent baseline selectors silently.
