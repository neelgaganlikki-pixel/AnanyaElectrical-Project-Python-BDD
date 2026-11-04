import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('reports/dom_analysis/app_bundle.js', 'r', encoding='utf-8') as f:
    js = f.read()

snippet = js[319500:321500]
print(snippet)

