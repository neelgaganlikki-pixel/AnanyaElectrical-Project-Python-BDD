import re

with open('reports/dom_analysis/app_bundle.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("File size:", len(js))

# Look for form submission handlers or quote-form
keywords = ["quote-form", "Submit Engineering Inquiry", "Enquiry Forms", "mailto:", "wa.me", "client-name", "client-phone", "project-type"]
for kw in keywords:
    pos = 0
    print(f"\n=== KEYWORD: {kw} ===")
    matches = [m.start() for m in re.finditer(re.escape(kw), js)]
    print(f"Found {len(matches)} occurrences")
    for p in matches[:3]:
        snippet = js[max(0, p-100):min(len(js), p+200)]
        print(f"[{p}] ... {snippet} ...\n")

