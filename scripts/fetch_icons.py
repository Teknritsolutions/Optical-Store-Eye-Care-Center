from pathlib import Path
from urllib.request import urlopen
out=Path('assets/icons');out.mkdir(exist_ok=True)
for name in ['eye','shield-check','glasses','scan-face','moon','sun','arrow-up-right']:
 data=urlopen('https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/'+name+'.svg',timeout=30).read();(out/(name+'.svg')).write_bytes(data)
(out/'LICENSE').write_bytes(urlopen('https://raw.githubusercontent.com/lucide-icons/lucide/main/LICENSE',timeout=30).read())
print('Saved seven Lucide SVG icons and ISC license.')
