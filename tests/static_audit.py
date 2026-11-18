"""Validate local links, HTML structure, section counts, image hashes, CSS syntax and labels."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from collections import Counter,defaultdict
from bs4 import BeautifulSoup
import hashlib,json,html5lib,tinycss2,sys
ROOT=Path(__file__).resolve().parents[1];failures=[];image_usage=defaultdict(set)
manifest=json.loads((ROOT/'scripts/page-manifest.json').read_text())
for file in (list(ROOT.glob('*.html'))+list((ROOT/'pages').glob('*.html')))+list((ROOT/'documentation').glob('*.html')):
 text=file.read_text();soup=BeautifulSoup(text,'html.parser');parser=html5lib.HTMLParser(strict=False);parser.parse(text)
 for pos,code,data in parser.errors:
  if code!='expected-doctype-but-got-start-tag':failures.append([str(file.relative_to(ROOT)),'HTML',pos,code,data])
 ids=[x.get('id') for x in soup.select('[id]')]
 for id,count in Counter(ids).items():
  if count>1:failures.append([file.name,'duplicate-id',id])
 if file.parent in (ROOT, ROOT/'pages') and file.name in manifest:
  count=len(soup.select('main > section'))
  if count!=manifest[file.name]['sections']:failures.append([file.name,'section-count',count])
  if len(soup.select('h1'))!=1:failures.append([file.name,'h1-count'])
 for el in soup.select('[href],[src]'):
  ref=el.get('href',el.get('src',''));url=urlsplit(ref)
  if url.scheme or url.netloc or ref.startswith('data:'):continue
  target=file.parent/unquote(url.path) if url.path else file
  if not target.exists():failures.append([file.name,'missing-target',ref])
  elif url.fragment and target.suffix=='.html':
   doc=soup if target==file else BeautifulSoup(target.read_text(),'html.parser')
   if not doc.find(id=unquote(url.fragment)):failures.append([file.name,'missing-anchor',ref])
 for el in soup.select('img'):
  if not el.get('alt'):failures.append([file.name,'image-alt',el.get('src')])
  # Gallery thumbnails are controls and intentionally share the gallery source.
  if not el.find_parent(class_='gallery-thumbs'):image_usage[el.get('src')].add(file.name)
 for el in soup.select('input,textarea,select'):
  if not soup.find('label',attrs={'for':el.get('id')}) and not el.find_parent('label'):failures.append([file.name,'missing-label',el.get('id')])
 css=ROOT/'assets/css/styles.css'
for rule in tinycss2.parse_stylesheet(css.read_text(),skip_whitespace=True,skip_comments=True):
 if rule.type=='error':failures.append(['CSS',rule.message])
hashes=defaultdict(list)
for f in (ROOT/'assets/images').glob('*.webp'):
 if '-480' not in f.stem:hashes[hashlib.sha256(f.read_bytes()).hexdigest()].append(f.name)
duplicates=[v for v in hashes.values() if len(v)>1]
if duplicates:failures.append(['duplicate-image-hashes',duplicates])
reused={src:sorted(pages) for src,pages in image_usage.items() if len(pages)>1}
if reused:failures.append(['reused-content-images',reused])
report={'pages':len(manifest),'html_files':len((list(ROOT.glob('*.html'))+list((ROOT/'pages').glob('*.html'))))+len(list((ROOT/'documentation').glob('*.html'))),'unique_webp_originals':len(hashes),'repeated_content_sources':reused,'duplicate_hashes':duplicates,'failures':failures}
(ROOT/'tests/artifacts/static-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));sys.exit(bool(failures))
