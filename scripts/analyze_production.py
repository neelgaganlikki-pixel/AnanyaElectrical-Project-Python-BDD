import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

PROD_URL = "https://ananyaelectricalsolutions.com/"
DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev/"
OUTPUT_DIR = os.path.join(os.getcwd(), "reports", "production_analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_production():
    print(f"=== INITIATING DEEP PRODUCTION ANALYSIS ===")
    print(f"Target URL: {PROD_URL}\n")
    
    analysis_data = {
        "url": PROD_URL,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "http_diagnostics": {},
        "console": [],
        "failed_requests": [],
        "requests_summary": {},
        "metadata": {},
        "structured_data": [],
        "headings": {},
        "navigation": {},
        "form_analysis": {},
        "integrations": {},
        "performance": {},
        "responsive": {},
        "security": {}
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080}, ignore_https_errors=False)
        page = context.new_page()

        # Capture console
        page.on("console", lambda msg: analysis_data["console"].append({
            "type": msg.type,
            "text": msg.text,
            "location": msg.location
        }))

        # Capture network
        all_requests = []
        page.on("request", lambda r: all_requests.append({
            "url": r.url,
            "method": r.method,
            "resource_type": r.resource_type
        }))

        page.on("requestfailed", lambda r: analysis_data["failed_requests"].append({
            "url": r.url,
            "method": r.method,
            "failure": str(r.failure)
        }))

        # 1. Navigation & HTTP Diagnostics
        start_time = time.time()
        response = page.goto(PROD_URL, wait_until="networkidle", timeout=45000)
        nav_duration = round(time.time() - start_time, 2)

        status_code = response.status if response else None
        headers = response.headers if response else {}
        
        analysis_data["http_diagnostics"] = {
            "status_code": status_code,
            "final_url": page.url,
            "server": headers.get("server", "Unknown"),
            "content_type": headers.get("content-type", "Unknown"),
            "content_encoding": headers.get("content-encoding", "None"),
            "cache_control": headers.get("cache-control", "None"),
            "security_headers": {
                "strict-transport-security": headers.get("strict-transport-security", "Not Set"),
                "x-content-type-options": headers.get("x-content-type-options", "Not Set"),
                "x-frame-options": headers.get("x-frame-options", "Not Set"),
                "content-security-policy": headers.get("content-security-policy", "Not Set"),
                "referrer-policy": headers.get("referrer-policy", "Not Set")
            },
            "total_requests": len(all_requests),
            "nav_duration_seconds": nav_duration
        }

        print(f"HTTP Status: {status_code} | Server: {headers.get('server')} | Total Network Requests: {len(all_requests)}")

        # 2. Performance Timing
        timing = page.evaluate("() => JSON.parse(JSON.stringify(window.performance.timing))")
        nav_entries = page.evaluate("() => performance.getEntriesByType('navigation')")
        fcp = page.evaluate("""() => {
            const paint = performance.getEntriesByType('paint');
            const fcpEntry = paint.find(p => p.name === 'first-contentful-paint');
            return fcpEntry ? Math.round(fcpEntry.startTime) : null;
        }""")

        connect_time = timing.get("connectEnd", 0) - timing.get("connectStart", 0)
        ttfb = timing.get("responseStart", 0) - timing.get("requestStart", 0)
        dom_content_loaded = timing.get("domContentLoadedEventEnd", 0) - timing.get("navigationStart", 0)
        load_event = timing.get("loadEventEnd", 0) - timing.get("navigationStart", 0)

        analysis_data["performance"] = {
            "ttfb_ms": ttfb,
            "tcp_connect_ms": connect_time,
            "dom_content_loaded_ms": dom_content_loaded,
            "load_event_ms": load_event,
            "first_contentful_paint_ms": fcp
        }
        print(f"Performance: TTFB={ttfb}ms | DCL={dom_content_loaded}ms | Load={load_event}ms | FCP={fcp}ms")

        # 3. Metadata, Title & SEO
        title = page.title()
        meta_desc = page.locator("meta[name='description']").get_attribute("content") if page.locator("meta[name='description']").count() else None
        meta_robots = page.locator("meta[name='robots']").get_attribute("content") if page.locator("meta[name='robots']").count() else None
        canonical = page.locator("link[rel='canonical']").get_attribute("href") if page.locator("link[rel='canonical']").count() else None
        
        # Social cards
        og_title = page.locator("meta[property='og:title']").get_attribute("content") if page.locator("meta[property='og:title']").count() else None
        og_image = page.locator("meta[property='og:image']").get_attribute("content") if page.locator("meta[property='og:image']").count() else None
        og_url = page.locator("meta[property='og:url']").get_attribute("content") if page.locator("meta[property='og:url']").count() else None
        twitter_card = page.locator("meta[name='twitter:card']").get_attribute("content") if page.locator("meta[name='twitter:card']").count() else None

        analysis_data["metadata"] = {
            "title": title,
            "title_length": len(title) if title else 0,
            "description": meta_desc,
            "description_length": len(meta_desc) if meta_desc else 0,
            "robots": meta_robots,
            "canonical": canonical,
            "og_title": og_title,
            "og_image": og_image,
            "og_url": og_url,
            "twitter_card": twitter_card
        }
        print(f"Title: {title} ({len(title)} chars)")
        print(f"Canonical URL: {canonical}")

        # 4. JSON-LD Structured Data
        json_ld_scripts = page.locator("script[type='application/ld+json']").all()
        for idx, s in enumerate(json_ld_scripts):
            try:
                content = json.loads(s.inner_text())
                analysis_data["structured_data"].append({
                    "index": idx,
                    "type": content.get("@type"),
                    "name": content.get("name"),
                    "schema": content
                })
            except Exception as e:
                pass
        print(f"Schema.org JSON-LD Schemas Found: {len(analysis_data['structured_data'])}")

        # 5. Headings Hierarchy
        h1s = [h.inner_text().strip() for h in page.locator("h1").all() if h.inner_text().strip()]
        h2s = [h.inner_text().strip() for h in page.locator("h2").all() if h.inner_text().strip()]
        h3s = [h.inner_text().strip() for h in page.locator("h3").all() if h.inner_text().strip()]
        analysis_data["headings"] = {
            "h1_count": len(h1s),
            "h1_text": h1s,
            "h2_count": len(h2s),
            "h2_text": h2s[:8],
            "h3_count": len(h3s)
        }
        print(f"Headings: H1={len(h1s)}, H2={len(h2s)}, H3={len(h3s)}")

        # 6. Navigation Elements
        nav_buttons = [b.inner_text().strip().replace('\n', ' ') for b in page.locator("header button").all() if b.inner_text().strip()]
        header_sticky = page.evaluate("""() => {
            const h = document.querySelector('header');
            return h ? window.getComputedStyle(h).position : 'none';
        }""")
        analysis_data["navigation"] = {
            "header_position": header_sticky,
            "header_buttons": nav_buttons
        }
        print(f"Header Buttons: {nav_buttons}")

        # 7. Modal Drawer (Enquiry Forms Hub)
        enquiry_btn = page.locator("header button:has-text('Enquiry Forms')").first
        if enquiry_btn.is_visible():
            enquiry_btn.click()
            page.wait_for_timeout(800)
            modal = page.locator("[role='dialog'][aria-modal='true']").first
            modal_visible = modal.is_visible()
            cards_count = modal.locator("span:has-text('Open Modal')").count()
            close_btn = modal.locator("button:has-text('close')").first
            if close_btn.is_visible():
                close_btn.click()
                page.wait_for_timeout(500)
            analysis_data["navigation"]["enquiry_hub"] = {
                "modal_accessible": modal_visible,
                "forms_count": cards_count
            }
            print(f"Enquiry Forms Hub: Modal={modal_visible}, Form Cards={cards_count}")

        # 8. Consultation Form Analysis (#quote-form)
        quote_form = page.locator("#quote-form").first
        if quote_form.is_visible():
            inputs = quote_form.locator("input, select, textarea").all()
            input_details = []
            for inp in inputs:
                input_details.append({
                    "id": inp.get_attribute("id"),
                    "name": inp.get_attribute("name"),
                    "type": inp.get_attribute("type") or inp.evaluate("el => el.tagName.toLowerCase()"),
                    "required": inp.get_attribute("required") is not None,
                    "placeholder": inp.get_attribute("placeholder")
                })
            analysis_data["form_analysis"] = {
                "form_present": True,
                "input_count": len(inputs),
                "inputs": input_details
            }
            print(f"Consultation Form: Present with {len(inputs)} inputs")

        # 9. Third-Party Integrations & Contact Channels
        wa_link = page.locator("a[href*='wa.me']").first.get_attribute("href") if page.locator("a[href*='wa.me']").count() else None
        tel_links = [a.get_attribute("href") for a in page.locator("a[href^='tel:']").all()]
        mailto_links = [a.get_attribute("href") for a in page.locator("a[href^='mailto:']").all()]
        maps_link = page.locator("a[href*='google.com/maps']").first.get_attribute("href") if page.locator("a[href*='google.com/maps']").count() else None
        maps_rel = page.locator("a[href*='google.com/maps']").first.get_attribute("rel") if page.locator("a[href*='google.com/maps']").count() else None

        analysis_data["integrations"] = {
            "whatsapp_href": wa_link,
            "tel_hrefs": list(set(tel_links)),
            "mailto_hrefs": list(set(mailto_links)),
            "maps_href": maps_link,
            "maps_rel": maps_rel
        }
        print(f"Integrations: WhatsApp={bool(wa_link)}, Tel={len(tel_links)}, Mailto={len(mailto_links)}, Maps={bool(maps_link)}")

        # 10. Security Checks
        external_links = page.locator("a[target='_blank']").all()
        unsafe_links = []
        for l in external_links:
            rel = l.get_attribute("rel") or ""
            href = l.get_attribute("href") or ""
            if "noopener" not in rel and "noreferrer" not in rel:
                unsafe_links.append(href)

        analysis_data["security"] = {
            "https_enforced": page.url.startswith("https://"),
            "unsafe_blank_targets_count": len(unsafe_links),
            "unsafe_blank_links": unsafe_links[:5]
        }
        print(f"Security: HTTPS={analysis_data['security']['https_enforced']} | Unsafe Tabnabbing Links={len(unsafe_links)}")

        # 11. Screenshots across viewports
        print("Capturing Responsive Screenshots...")
        page.screenshot(path=os.path.join(OUTPUT_DIR, "production_desktop_1920.png"), full_page=True)

        # Tablet
        page.set_viewport_size({"width": 768, "height": 1024})
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "production_tablet_768.png"), full_page=True)

        # Mobile
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "production_mobile_375.png"), full_page=True)
        hamburger_visible = page.locator("header button:has-text('menu')").first.is_visible()
        analysis_data["responsive"]["mobile_hamburger_visible"] = hamburger_visible
        print(f"Responsive: Mobile Hamburger Visible={hamburger_visible}")

        # Save HTML page source
        with open(os.path.join(OUTPUT_DIR, "production_page_source.html"), "w", encoding="utf-8") as f:
            f.write(page.content())

        # Save Full Analysis JSON
        with open(os.path.join(OUTPUT_DIR, "production_analysis.json"), "w", encoding="utf-8") as f:
            json.dump(analysis_data, f, indent=2)

        browser.close()

    print(f"\n=== PRODUCTION ANALYSIS COMPLETE ===")
    print(f"Artifacts saved in: {OUTPUT_DIR}")
    return analysis_data

if __name__ == "__main__":
    analyze_production()

