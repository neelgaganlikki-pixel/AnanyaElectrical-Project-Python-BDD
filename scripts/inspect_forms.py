import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('reports/dom_analysis/dom_analysis.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

dom = d['dom_data']
print('=== FORMS DETAIL ===')
for i, f in enumerate(dom['forms']):
    print(f"Form #{i}: id={f['id']} action={f['action']} method={f['method']} class={f['class']}")
    for inp in f['inputs']:
        print(f"   tag={inp['tag']} type={inp['type']} name={inp['name']} id={inp['id']} req={inp['required']} ph='{inp['placeholder']}'")

print('\n=== ALL INPUTS & TEXTAREAS ===')
for inp in dom['inputs']:
    print(f"tag={inp['tag']} type={inp['type']} id={inp['id']} name={inp['name']} req={inp['required']} ph='{inp['placeholder']}' label='{inp['label']}'")

print('\n=== BUTTONS ===')
for i, b in enumerate(dom['buttons']):
    print(f"Button #{i}: text='{b['text']}' tag={b['tag']} id={b['id']} type={b['type']} class={b['class']}")

print('\n=== EXTERNAL INTEGRATIONS ===')
for ext in dom['external_integrations']:
    print(f"Ext: '{ext['text']}' -> {ext['href']}")

