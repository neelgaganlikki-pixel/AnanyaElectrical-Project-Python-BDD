import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('reports/dom_analysis/app_bundle.js', 'r', encoding='utf-8') as f:
    js = f.read()

snippet = js[318000:329000]
print(snippet)

