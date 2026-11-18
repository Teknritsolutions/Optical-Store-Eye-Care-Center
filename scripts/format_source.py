"""Optional development formatter. Requirements: beautifulsoup4, cssbeautifier, jsbeautifier."""
from pathlib import Path
from bs4 import BeautifulSoup
import cssbeautifier,jsbeautifier
ROOT=Path(__file__).resolve().parents[1]
for path in list(ROOT.glob('*.html'))+list((ROOT/'documentation').glob('*.html')):
 soup=BeautifulSoup(path.read_text(),'html.parser')
 for script in soup.find_all('script'):
  if not script.get('src') and script.string:script.string=jsbeautifier.beautify(script.string)
 path.write_text(soup.prettify(formatter='minimal'))
for path in (ROOT/'assets/css').glob('*.css'):path.write_text(cssbeautifier.beautify(path.read_text(),{'indent_size':2})+'\n')
for path in (ROOT/'assets/js').glob('*.js'):path.write_text(jsbeautifier.beautify(path.read_text(),{'indent_size':2})+'\n')
print('Formatted HTML, CSS and JavaScript sources.')
