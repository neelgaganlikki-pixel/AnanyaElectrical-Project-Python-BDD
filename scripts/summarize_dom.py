import json

with open('reports/dom_analysis/dom_analysis.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== BASIC INFO ===')
print('Title:', d['title'])
print('Status:', d['status_code'])
print('Console messages count:', len(d['console_messages']))
for cm in d['console_messages']:
    print('  Console:', cm['type'], cm['text'][:120])
print('Failed requests count:', len(d['failed_requests']))
for fr in d['failed_requests']:
    print('  Failed req:', fr['url'], fr.get('failure'))

dom = d['dom_data']
print('\n=== SECTIONS ===')
for s in dom['sections']:
    print(f"Tag: {s['tag']}, ID: {s['id']}, Class: {s['class']}, Heading: {s['heading']}")

print('\n=== NAVIGATION LINKS ===')
for n in dom['navigation']:
    print(f"Nav: '{n['text']}' -> {n['href']}")

print('\n=== HEADINGS ===')
for h in dom['headings']:
    print(f"{h['tag']}: {h['text']}")

print('\n=== FORMS ===')
for f in dom['forms']:
    print(f"Form ID: {f['id']}, Action: {f['action']}, Method: {f['method']}, Class: {f['class']}")
    for inp in f['inputs']:
        print(f"  Input: {inp['tag']} type={inp['type']} name={inp['name']} id={inp['id']} req={inp['required']} ph='{inp['placeholder']}' label='{inp['label']}'")

print('\n=== ALL INPUTS ===')
for inp in dom['inputs']:
    print(f"Input: tag={inp['tag']} type={inp['type']} id={inp['id']} name={inp['name']} req={inp['required']} ph='{inp['placeholder']}' minlen={inp['minlength']} maxlen={inp['maxlength']} pattern={inp['pattern']}")

print('\n=== BUTTONS ===')
for b in dom['buttons']:
    print(f"Button: text='{b['text']}' tag={b['tag']} id={b['id']} class={b['class']} type={b['type']}")

print('\n=== CONTACT LINKS ===')
print('WhatsApp:', json.dumps(dom['contact_links']['whatsapp'], indent=2))
print('Tel:', json.dumps(dom['contact_links']['tel'], indent=2))
print('Mailto:', json.dumps(dom['contact_links']['mailto'], indent=2))

print('\n=== EXTERNAL INTEGRATIONS ===')
for ext in dom['external_integrations']:
    print(f"Ext: '{ext['text']}' -> {ext['href']}")

print('\n=== IMAGES COUNT ===', len(dom['images']))
for img in dom['images'][:10]:
    print('Img:', img.get('src') or img.get('class'), 'Alt:', img.get('alt'))

