"""Reliable full-page captures via a tall viewport (avoids Chrome captureBeyondViewport tiling)."""
import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/artifacts'
async def main():
 files=json.loads((ROOT/'scripts/page-manifest.json').read_text())
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
  page=await browser.new_page(color_scheme='light',reduced_motion='reduce')
  for file in files:
   if len(sys.argv)>1 and file not in sys.argv[1:]:continue
   await page.set_viewport_size({'width':1440,'height':1000});await page.goto('http://127.0.0.1:8765/'+("pages/"+file));await page.evaluate('document.fonts.ready')
   await page.evaluate("async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))}")
   for width,theme,direction in [(390,'light','ltr'),(820,'light','ltr'),(1440,'light','ltr'),(390,'dark','rtl'),(1440,'dark','rtl')]:
    await page.evaluate('([t,d])=>{document.documentElement.dataset.theme=t;document.documentElement.dir=d;scrollTo(0,0)}',[theme,direction]);await page.set_viewport_size({'width':width,'height':1000});await page.wait_for_timeout(100)
    height=await page.evaluate('document.documentElement.scrollHeight');await page.set_viewport_size({'width':width,'height':height});await page.wait_for_timeout(180);await page.screenshot(path=str(OUT/f'{file[:-5]}-{width}-{theme}-{direction}.png'))
   print('Captured',file,flush=True)
  await browser.close()
asyncio.run(main())
