"""Shared paths for all website pages."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def page_path(name):
 return 'pages/' + name
def write_page(name, html):
 target = ROOT / page_path(name)
 target.parent.mkdir(exist_ok=True)
 breadcrumb = re.search(r'<nav[^>]*class="breadcrumbs container"[^>]*>[\s\S]*?</nav>', html)
 if breadcrumb:
  html = html.replace(breadcrumb.group(0), '')
  html = re.sub(r'(<main[^>]*>\s*<section[^>]*>)', lambda match: match.group(1) + breadcrumb.group(0), html, count=1)
 def reference(match):
  attr, quote, value = match.groups()
  if value.startswith('documentation/'): value = '../' + value
  value = re.sub(r'(^|,\s*)assets/', r'\1../assets/', value)
  return attr + '=' + quote + value + quote
 html = re.sub(r'''\b(href|src|srcset)=(["'])(.*?)\2''', reference, html)
 html = html.replace(chr(8594), "<svg class=\"ui-icon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M4 12h16m-6-6 6 6-6 6\"/></svg>").replace(chr(8592), "<svg class=\"ui-icon\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"M20 12H4m6-6-6 6 6 6\"/></svg>")
 html = html.replace('<span aria-hidden="true">' + chr(8964) + '</span>', "<svg class=\"ui-icon nav-chevron\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"m6 9 6 6 6-6\"/></svg>")
 for initial, person in [('A','amelia'), ('D','daniel'), ('S','sofia'), ('O','oliver')]:
  html = re.sub(r'<span class="avatar">\s*' + initial + r'\s*</span>', '<img class="avatar testimonial-portrait" src="../assets/images/testimonial-' + person + '.webp" alt="" width="56" height="56" loading="lazy">', html)
 if name not in ('index.html', 'home-2.html', 'sitemap.html') and '<body class="inner-page"' not in html:
  html = html.replace('<body', '<body class="inner-page"', 1)
 target.write_text(html, encoding='utf-8')
