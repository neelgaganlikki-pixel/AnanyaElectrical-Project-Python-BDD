"""
Comprehensive Live Analyzer for https://ananyaelectricalsolutions.com/
Extracts full architectural, technical, DOM, network, content, and interactive data.
"""
import json
import time
from playwright.sync_api import sync_playwright

def analyze_full_site():
    url = "https://ananyaelectricalsolutions.com/"
    print(f"Starting deep analysis of {url}...")
    
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Track network requests
        network_requests = []
        failed_requests = []
        page.on("request", lambda req: network_requests.append({
            "url": req.url,
            "resource_type": req.resource_type,
            "method": req.method
        }))
        page.on("requestfailed", lambda req: failed_requests.append({
            "url": req.url,
            "failure": req.failure
        }))
        
        # Track console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append({
            "type": msg.type,
            "text": msg.text
        }))
        
        t0 = time.time()
        response = page.goto(url, wait_until="networkidle", timeout=45000)
        load_time = time.time() - t0
        
        # HTTP diagnostics
        results["http"] = {
            "status": response.status if response else None,
            "url": response.url if response else None,
            "headers": response.headers if response else {},
            "load_time_sec": round(load_time, 2)
        }
        
        # Performance timing
        perf_data = page.evaluate("""() => {
            const timing = window.performance.timing;
            const nav = window.performance.getEntriesByType('navigation')[0] || {};
            return {
                ttfb: nav.responseStart ? Math.round(nav.responseStart - nav.requestStart) : (timing.responseStart - timing.requestStart),
                domContentLoaded: nav.domContentLoadedEventEnd ? Math.round(nav.domContentLoadedEventEnd - nav.startTime) : (timing.domContentLoadedEventEnd - timing.navigationStart),
                loadEvent: nav.loadEventEnd ? Math.round(nav.loadEventEnd - nav.startTime) : (timing.loadEventEnd - timing.navigationStart),
                transferSize: nav.transferSize || null,
                decodedBodySize: nav.decodedBodySize || null
            };
        }""")
        results["performance"] = perf_data
        
        # Title and Meta tags
        meta_data = page.evaluate("""() => {
            const getMeta = (name) => {
                const el = document.querySelector(`meta[name='${name}']`) || document.querySelector(`meta[property='${name}']`);
                return el ? el.getAttribute('content') : null;
            };
            const canonical = document.querySelector("link[rel='canonical']");
            return {
                title: document.title,
                description: getMeta('description'),
                canonical: canonical ? canonical.getAttribute('href') : null,
                robots: getMeta('robots'),
                og_title: getMeta('og:title'),
                og_description: getMeta('og:description'),
                og_image: getMeta('og:image'),
                og_url: getMeta('og:url'),
                twitter_card: getMeta('twitter:card'),
                viewport: getMeta('viewport')
            };
        }""")
        results["metadata"] = meta_data
        
        # Structured Data JSON-LD
        structured_data = page.evaluate("""() => {
            const scripts = Array.from(document.querySelectorAll("script[type='application/ld+json']"));
            return scripts.map(s => {
                try {
                    return JSON.parse(s.innerText);
                } catch(e) {
                    return { error: e.toString() };
                }
            });
        }""")
        results["structured_data"] = structured_data
        
        # Heading Structure
        headings = page.evaluate("""() => {
            return {
                h1: Array.from(document.querySelectorAll('h1')).map(el => el.innerText.trim()),
                h2: Array.from(document.querySelectorAll('h2')).map(el => el.innerText.trim()),
                h3: Array.from(document.querySelectorAll('h3')).map(el => el.innerText.trim()).slice(0, 20),
                h3_count: document.querySelectorAll('h3').length
            };
        }""")
        results["headings"] = headings
        
        # Header navigation and buttons
        nav_elements = page.evaluate("""() => {
            const buttons = Array.from(document.querySelectorAll('header button, header a')).map(el => ({
                text: el.innerText.replace(/\\s+/g, ' ').trim(),
                tag: el.tagName.toLowerCase(),
                href: el.getAttribute('href') || null,
                id: el.id || null,
                className: el.className || null
            }));
            return buttons;
        }""")
        results["navigation"] = nav_elements
        
        # Form structure and fields
        forms_info = page.evaluate("""() => {
            const forms = Array.from(document.querySelectorAll('form')).map((f, i) => {
                const inputs = Array.from(f.querySelectorAll('input, select, textarea, button')).map(inp => ({
                    tag: inp.tagName.toLowerCase(),
                    type: inp.getAttribute('type') || (inp.tagName.toLowerCase() === 'textarea' ? 'textarea' : (inp.tagName.toLowerCase() === 'select' ? 'select' : null)),
                    id: inp.id || null,
                    name: inp.name || null,
                    placeholder: inp.placeholder || null,
                    required: inp.required,
                    checked: inp.checked || false,
                    value: inp.value || null,
                    text: inp.innerText.trim() || null
                }));
                return {
                    formIndex: i,
                    action: f.getAttribute('action'),
                    method: f.getAttribute('method'),
                    id: f.id || null,
                    inputs: inputs
                };
            });
            return forms;
        }""")
        results["forms"] = forms_info
        
        # Links and Integrations
        links_info = page.evaluate("""() => {
            const allLinks = Array.from(document.querySelectorAll('a')).map(a => ({
                text: a.innerText.replace(/\\s+/g, ' ').trim(),
                href: a.getAttribute('href') || '',
                target: a.getAttribute('target') || null,
                rel: a.getAttribute('rel') || null
            }));
            
            const telLinks = allLinks.filter(l => l.href.startsWith('tel:'));
            const mailtoLinks = allLinks.filter(l => l.href.startsWith('mailto:'));
            const whatsappLinks = allLinks.filter(l => l.href.includes('wa.me') || l.href.includes('whatsapp.com'));
            const mapsLinks = allLinks.filter(l => l.href.includes('google.com/maps'));
            const externalLinks = allLinks.filter(l => l.href.startsWith('http') && !l.href.includes('ananyaelectricalsolutions.com'));
            
            return {
                total_links: allLinks.length,
                tel: telLinks,
                mailto: mailtoLinks,
                whatsapp: whatsappLinks,
                maps: mapsLinks,
                external: externalLinks
            };
        }""")
        results["links_and_integrations"] = links_info
        
        # Enquiry forms hub inspection
        hub_data = page.evaluate("""() => {
            const hubBtn = Array.from(document.querySelectorAll('header button')).find(b => b.innerText.includes('Enquiry Forms'));
            return {
                hub_button_found: !!hubBtn,
                hub_button_text: hubBtn ? hubBtn.innerText.trim() : null
            };
        }""")
        
        # If hub button found, click and inspect cards
        if hub_data.get("hub_button_found"):
            page.click("header button:has-text('Enquiry Forms')")
            page.wait_for_timeout(1000)
            
            modal_info = page.evaluate("""() => {
                const dialog = document.querySelector('[role="dialog"][aria-modal="true"]');
                if (!dialog) return { open: false };
                
                const cards = Array.from(dialog.querySelectorAll('span')).filter(s => s.innerText.includes('Open Modal')).map(s => {
                    const cardParent = s.closest('div.border') || s.closest('div.rounded') || s.parentElement;
                    const titleEl = cardParent ? cardParent.querySelector('h3, h4, div.font-bold, div.font-semibold, p.font-bold') : null;
                    return {
                        title: titleEl ? titleEl.innerText.trim() : 'Modular Form Card',
                        button_text: s.innerText.trim()
                    };
                });
                
                const allHeadings = Array.from(dialog.querySelectorAll('h2, h3, h4')).map(h => h.innerText.trim());
                
                return {
                    open: true,
                    dialog_headings: allHeadings,
                    cards_count: cards.length,
                    cards: cards
                };
            }""")
            results["enquiry_hub_drawer"] = modal_info
            # Close dialog
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        else:
            results["enquiry_hub_drawer"] = {"open": false}
            
        # Inspect 3D Models dropdown & section
        models_3d = page.evaluate("""() => {
            const modelBtn = Array.from(document.querySelectorAll('header button')).find(b => b.innerText.includes('3D Model'));
            const canvasEl = document.querySelector('canvas');
            return {
                model_nav_found: !!modelBtn,
                canvas_found_in_dom: !!canvasEl,
                canvas_width: canvasEl ? canvasEl.width : null,
                canvas_height: canvasEl ? canvasEl.height : null
            };
        }""")
        results["three_d_models"] = models_3d
        
        # FAQ details
        faqs = page.evaluate("""() => {
            // Find FAQ questions/accordions
            const faqSection = Array.from(document.querySelectorAll('section, div')).find(el => {
                const h = el.querySelector('h2, h3');
                return h && (h.innerText.toLowerCase().includes('faq') || h.innerText.toLowerCase().includes('frequently asked'));
            });
            
            const questions = Array.from(document.querySelectorAll('button, div')).filter(el => {
                const txt = el.innerText.trim();
                return txt.endsWith('?') && (txt.includes('Super Grade') || txt.includes('BESCOM') || txt.includes('CEIG') || txt.includes('Solar') || txt.includes('Where is'));
            }).map(el => el.innerText.trim());
            
            return {
                faq_questions_detected: Array.from(new Set(questions))
            };
        }""")
        results["faqs"] = faqs
        
        # Images audit
        images_info = page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
                src: img.src,
                alt: img.alt || '',
                naturalWidth: img.naturalWidth,
                naturalHeight: img.naturalHeight,
                complete: img.complete
            }));
            const brokenImages = imgs.filter(img => !img.complete || img.naturalWidth === 0);
            return {
                total_images: imgs.length,
                broken_images_count: brokenImages.length,
                broken_images: brokenImages,
                sample_images: imgs.slice(0, 10)
            };
        }""")
        results["images"] = images_info
        
        # Summary of assets
        asset_summary = {}
        for req in network_requests:
            rt = req["resource_type"]
            asset_summary[rt] = asset_summary.get(rt, 0) + 1
        results["network_summary"] = {
            "total_requests": len(network_requests),
            "asset_types": asset_summary,
            "failed_requests": failed_requests,
            "console_messages": console_messages
        }
        
        browser.close()
        
    out_file = "reports/production_analysis/complete_site_analysis.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print(f"Analysis saved to {out_file} successfully!")
    return results

if __name__ == "__main__":
    analyze_full_site()

