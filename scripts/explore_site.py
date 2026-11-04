import json
import os
import sys
from playwright.sync_api import sync_playwright

DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev"
OUTPUT_DIR = os.path.join(os.getcwd(), "reports", "dom_analysis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def explore():
    print(f"Launching exploration for: {DEV_URL}")
    console_messages = []
    network_requests = []
    failed_requests = []
    redirects = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Listen to console
        def on_console(msg):
            console_messages.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            })
        page.on("console", on_console)

        # Listen to network requests/responses
        def on_request(request):
            network_requests.append({
                "url": request.url,
                "method": request.method,
                "resource_type": request.resource_type
            })

        def on_request_failed(request):
            failed_requests.append({
                "url": request.url,
                "failure": request.failure,
                "method": request.method
            })

        def on_response(response):
            if 300 <= response.status < 400:
                redirects.append({
                    "url": response.url,
                    "status": response.status,
                    "headers": response.headers
                })

        page.on("request", on_request)
        page.on("requestfailed", on_request_failed)
        page.on("response", on_response)

        response = page.goto(DEV_URL, wait_until="networkidle", timeout=45000)
        status_code = response.status if response else None

        # Basic metadata
        title = page.title()
        current_url = page.url

        # Deep DOM extraction via JavaScript
        dom_data = page.evaluate('''() => {
            const data = {
                metadata: {},
                headings: [],
                sections: [],
                navigation: [],
                forms: [],
                inputs: [],
                buttons: [],
                links: [],
                images: [],
                contact_links: {
                    whatsapp: [],
                    tel: [],
                    mailto: []
                },
                external_integrations: [],
                all_interactive_elements: []
            };

            // Metadata
            data.metadata.title = document.title;
            data.metadata.meta_tags = Array.from(document.querySelectorAll('meta')).map(m => {
                const attrs = {};
                for (let a of m.attributes) attrs[a.name] = a.value;
                return attrs;
            });
            const canonical = document.querySelector('link[rel="canonical"]');
            data.metadata.canonical = canonical ? canonical.getAttribute('href') : null;

            // Headings
            document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
                data.headings.push({
                    tag: h.tagName.toLowerCase(),
                    text: h.innerText.trim(),
                    id: h.id || null,
                    class: h.className || null
                });
            });

            // Sections
            document.querySelectorAll('section, main, header, footer, div[id], [role="region"]').forEach(s => {
                if (s.tagName === 'SECTION' || s.id || s.getAttribute('role') === 'region' || s.tagName === 'HEADER' || s.tagName === 'FOOTER') {
                    data.sections.push({
                        tag: s.tagName.toLowerCase(),
                        id: s.id || null,
                        class: s.className || null,
                        role: s.getAttribute('role') || null,
                        aria_label: s.getAttribute('aria-label') || null,
                        heading: s.querySelector('h1, h2, h3, h4')?.innerText?.trim() || null
                    });
                }
            });

            // Navigation
            document.querySelectorAll('nav a, header a').forEach(a => {
                data.navigation.push({
                    text: a.innerText.trim(),
                    href: a.getAttribute('href'),
                    class: a.className,
                    id: a.id || null,
                    role: a.getAttribute('role') || null
                });
            });

            // Forms
            document.querySelectorAll('form').forEach(f => {
                const inputs = Array.from(f.querySelectorAll('input, textarea, select, button')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || null,
                    name: el.name || null,
                    id: el.id || null,
                    placeholder: el.placeholder || null,
                    required: el.required || false,
                    class: el.className || null,
                    label: el.labels && el.labels.length > 0 ? el.labels[0].innerText.trim() : null,
                    aria_label: el.getAttribute('aria-label') || null
                }));
                data.forms.push({
                    id: f.id || null,
                    name: f.name || null,
                    action: f.action || null,
                    method: f.method || null,
                    class: f.className || null,
                    inputs: inputs
                });
            });

            // All inputs (including outside form)
            document.querySelectorAll('input, textarea, select').forEach(el => {
                let labelText = el.labels && el.labels.length > 0 ? el.labels[0].innerText.trim() : null;
                if (!labelText && el.id) {
                    const l = document.querySelector(`label[for="${el.id}"]`);
                    if (l) labelText = l.innerText.trim();
                }
                data.inputs.push({
                    tag: el.tagName.toLowerCase(),
                    type: el.type || 'text',
                    id: el.id || null,
                    name: el.name || null,
                    placeholder: el.placeholder || null,
                    class: el.className || null,
                    required: el.required || false,
                    pattern: el.pattern || null,
                    minlength: el.minLength !== -1 ? el.minLength : null,
                    maxlength: el.maxLength !== -1 ? el.maxLength : null,
                    label: labelText,
                    aria_label: el.getAttribute('aria-label') || null,
                    value: el.value || ''
                });
            });

            // Buttons
            document.querySelectorAll('button, input[type="button"], input[type="submit"], [role="button"]').forEach(b => {
                data.buttons.push({
                    tag: b.tagName.toLowerCase(),
                    id: b.id || null,
                    class: b.className || null,
                    type: b.type || null,
                    text: (b.innerText || b.value || '').trim(),
                    role: b.getAttribute('role') || 'button',
                    aria_label: b.getAttribute('aria-label') || null,
                    disabled: b.disabled || false
                });
            });

            // Links
            document.querySelectorAll('a').forEach(a => {
                const href = a.getAttribute('href') || '';
                const item = {
                    text: a.innerText.trim(),
                    href: href,
                    id: a.id || null,
                    class: a.className || null,
                    title: a.getAttribute('title') || null,
                    target: a.getAttribute('target') || null,
                    aria_label: a.getAttribute('aria-label') || null
                };
                data.links.push(item);

                if (href.includes('wa.me') || href.includes('whatsapp.com')) {
                    data.contact_links.whatsapp.push(item);
                } else if (href.startsWith('tel:')) {
                    data.contact_links.tel.push(item);
                } else if (href.startsWith('mailto:')) {
                    data.contact_links.mailto.push(item);
                }

                if (href.startsWith('http') && !href.includes(window.location.hostname)) {
                    data.external_integrations.push({
                        href: href,
                        text: item.text,
                        target: item.target
                    });
                }
            });

            // Images
            document.querySelectorAll('img, svg').forEach(img => {
                if (img.tagName.toLowerCase() === 'img') {
                    data.images.push({
                        tag: 'img',
                        src: img.getAttribute('src'),
                        alt: img.getAttribute('alt'),
                        id: img.id || null,
                        class: img.className || null,
                        width: img.naturalWidth || img.width || null,
                        height: img.naturalHeight || img.height || null,
                        loading: img.getAttribute('loading') || null
                    });
                } else {
                    data.images.push({
                        tag: 'svg',
                        class: img.getAttribute('class') || null,
                        id: img.id || null,
                        aria_label: img.getAttribute('aria-label') || null,
                        role: img.getAttribute('role') || null
                    });
                }
            });

            return data;
        }''')

        # Take screenshots across desktop, tablet, mobile
        screenshots = {}
        # Desktop
        desktop_path = os.path.join(OUTPUT_DIR, "screenshot_desktop_1920.png")
        page.screenshot(path=desktop_path, full_page=True)
        screenshots["desktop_1920"] = desktop_path

        # Tablet 768x1024
        context_tablet = browser.new_context(viewport={"width": 768, "height": 1024})
        page_tablet = context_tablet.new_page()
        page_tablet.goto(DEV_URL, wait_until="networkidle")
        tablet_path = os.path.join(OUTPUT_DIR, "screenshot_tablet_768.png")
        page_tablet.screenshot(path=tablet_path, full_page=True)
        screenshots["tablet_768"] = tablet_path
        context_tablet.close()

        # Mobile 375x812
        context_mobile = browser.new_context(viewport={"width": 375, "height": 812})
        page_mobile = context_mobile.new_page()
        page_mobile.goto(DEV_URL, wait_until="networkidle")
        mobile_path = os.path.join(OUTPUT_DIR, "screenshot_mobile_375.png")
        page_mobile.screenshot(path=mobile_path, full_page=True)
        screenshots["mobile_375"] = mobile_path
        context_mobile.close()

        # Get outer HTML for detailed inspection
        html_content = page.content()
        with open(os.path.join(OUTPUT_DIR, "page_source.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        full_analysis = {
            "target_url": DEV_URL,
            "resolved_url": current_url,
            "status_code": status_code,
            "title": title,
            "console_messages": console_messages,
            "network_requests_count": len(network_requests),
            "failed_requests": failed_requests,
            "redirects": redirects,
            "dom_data": dom_data,
            "screenshots": screenshots
        }

        json_path = os.path.join(OUTPUT_DIR, "dom_analysis.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(full_analysis, f, indent=2, ensure_ascii=False)

        print(f"DOM analysis saved to: {json_path}")
        browser.close()
        return full_analysis

if __name__ == "__main__":
    explore()

