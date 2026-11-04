from bs4 import BeautifulSoup
import json

with open("reports/dom_analysis/page_source.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Title:", soup.title.string if soup.title else "No title")

# All sections with IDs
print("\n--- SECTIONS WITH IDS ---")
for sec in soup.find_all(["section", "div", "main"], id=True):
    print(f"ID: #{sec['id']}, Tag: <{sec.name}>, Classes: {sec.get('class', [])}")

# All forms and inputs
print("\n--- FORMS & FIELDS ---")
for i, form in enumerate(soup.find_all("form")):
    print(f"Form #{i}: id={form.get('id')} action={form.get('action')} method={form.get('method')}")
    for el in form.find_all(["input", "select", "textarea", "button"]):
        print(f"  <{el.name}> type={el.get('type')} id={el.get('id')} name={el.get('name')} req={el.has_attr('required')} ph='{el.get('placeholder')}' text='{el.get_text(strip=True)[:40]}'")

# All Modals / Hidden Dialogs / Templates
print("\n--- DIALOGS / MODALS / DRAWERS ---")
for el in soup.find_all(attrs={"role": ["dialog", "menu", "region", "alert"]}):
    print(f"Role: {el.get('role')} id={el.get('id')} class={el.get('class', [])[:3]}")

# Script tags to see if React / Next.js / Vite / Tailwind
print("\n--- SCRIPTS & FRAMEWORK ---")
for script in soup.find_all("script"):
    src = script.get("src")
    if src:
        print("Script src:", src)
    elif script.string and ("__INITIAL_STATE__" in script.string or "React" in script.string or "vite" in script.string):
        print("Inline script with data...")

# Meta tags
print("\n--- META TAGS ---")
for m in soup.find_all("meta"):
    print(m.attrs)

