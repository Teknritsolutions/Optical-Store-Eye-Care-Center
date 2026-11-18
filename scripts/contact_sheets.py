from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
out=Path('tests/artifacts')
for width,theme,direction in [(1440,'light','ltr'),(390,'light','ltr'),(1440,'dark','rtl'),(390,'dark','rtl')]:
 files=sorted(out.glob(f'*-{width}-{theme}-{direction}.png'))
 for part in range(0,len(files),4):
  selected=files[part:part+4];cellw=320;thumbs=[]
  for f in selected:
   im=Image.open(f);im.resize((cellw,round(im.height*cellw/im.width))).save(out/(f.stem+'-thumb.png'))
   im=Image.open(out/(f.stem+'-thumb.png'));thumbs.append(im)
  h=max(im.height for im in thumbs)+32
  sheet=Image.new('RGB',(cellw*len(thumbs),h),'#d9dddc');d=ImageDraw.Draw(sheet)
  for i,(f,im) in enumerate(zip(selected,thumbs)):
   sheet.paste(im,(i*cellw,32));d.text((i*cellw+5,8),f.name.replace('.png',''),fill='#173b45')
  sheet.save(out/f'contact-{width}-{theme}-{direction}-{part//4}.jpg',quality=86)
print('Built page contact sheets.')
