import re

with open('reports/dom_analysis/page_source.html', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'src=["\']([^"\']*\.js)["\']', html)
print('Script paths:', matches)

