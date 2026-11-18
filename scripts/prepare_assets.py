"""Optimise original generated photographs; build deterministic vector brand assets."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'assets/images'
manifest=json.loads((ROOT/'scripts/generated-assets.json').read_text())
manifest.update(json.loads((ROOT/'scripts/generated-assets-extra.json').read_text()))
for name,source in manifest.items():
 target=out/(name+'.webp')
 if target.exists():continue
 im=Image.open(source).convert('RGB');im.thumbnail((1200,1200));im.save(target,'WEBP',quality=85,method=6)
 small=im.copy();small.thumbnail((480,480));small.save(out/(name+'-480.webp'),'WEBP',quality=80,method=6)
for mode,color in [('light','#173B45'),('dark','#F4F6F5')]:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64" fill="none"><g stroke="{color}" stroke-width="2"><path d="M3 32S11 19 26 19s23 13 23 13-8 13-23 13S3 32 3 32Z"/><circle cx="26" cy="32" r="8"/><path d="M26 24v16" stroke-width="1"/></g><text x="61" y="40" fill="{color}" font-family="Manrope,Arial,sans-serif" font-size="36" letter-spacing="-2">oculis</text><text x="63" y="55" fill="{color}" font-family="Manrope,Arial,sans-serif" font-size="7" letter-spacing="1.3">EYEWEAR &amp; EYE CARE</text></svg>'''
 (out/f'logo-{mode}.svg').write_text(svg)
favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#173B45"/><g fill="none" stroke="#C5A47E" stroke-width="2"><path d="M6 32s9-15 26-15 26 15 26 15-9 15-26 15S6 32 6 32Z"/><circle cx="32" cy="32" r="10"/><path d="M32 22v20" stroke-width="1"/></g></svg>'
(out/'favicon.svg').write_text(favicon)
im=Image.new('RGB',(256,256),'#173B45');d=ImageDraw.Draw(im);d.line([(24,128),(40,104),(72,80),(104,68),(128,64),(152,68),(184,80),(216,104),(232,128),(216,152),(184,176),(152,188),(128,192),(104,188),(72,176),(40,152),(24,128)],fill='#C5A47E',width=8);d.ellipse((88,88,168,168),outline='#C5A47E',width=7);d.line((128,88,128,168),fill='#C5A47E',width=4)
im.save(out/'favicon.ico',sizes=[(16,16),(32,32),(48,48)]);im.resize((180,180)).save(out/'apple-touch-icon.png')
print('Prepared',len(manifest),'original images plus responsive derivatives and brand assets.')
