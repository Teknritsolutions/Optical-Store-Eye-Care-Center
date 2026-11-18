import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
REFS={
 'farm':'https://teknritsolutions-2.github.io/Local-Farm-or-Community-Supported-Agriculture-CSA-/pages/public/index.html',
 'events':'https://teknrit-maker.github.io/High-End-Event-Planning/pages/index.html',
 'bookstore':'https://teknrit-maker.github.io/Local-Indie-Bookstore/pages/index.html',
 'food':'https://teknrit-maker.github.io/FoodTruck/Pages/menu.html',
 'yarn':'https://ravivarmaadepu123.github.io/boutique-yarn-and-craft-supply/pages/'}
OUT=Path('tests/artifacts/references');OUT.mkdir(parents=True,exist_ok=True)
async def main():
 report={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-sandbox'])
  page=await browser.new_page()
  for name,url in REFS.items():
   try:
    await page.goto(url,wait_until='domcontentloaded',timeout=45000);await page.wait_for_timeout(1200)
    record={'title':await page.title(),'headings':await page.locator('h1,h2').all_text_contents(),'widths':{}}
    for width in [1440,820,390]:
     await page.set_viewport_size({'width':width,'height':1000});await page.screenshot(path=str(OUT/f'{name}-{width}.png'),full_page=False);record['widths'][width]=await page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})')
    links=await page.locator('a').evaluate_all("els=>els.map(a=>({text:a.textContent.trim(),href:a.href})).filter(a=>/about|products|services/i.test(a.text)).slice(0,2)")
    record['linked_pages']=[]
    for link in links:
     try:
      await page.goto(link['href'],wait_until='domcontentloaded',timeout=30000);record['linked_pages'].append({'url':link['href'],'title':await page.title(),'headings':await page.locator('h1,h2').all_text_contents()})
     except Exception as e:record['linked_pages'].append({'url':link['href'],'error':str(e)})
    report[name]=record;print(name,'reviewed',flush=True)
   except Exception as e:report[name]={'error':str(e)}
  await browser.close()
 (OUT/'review.json').write_text(json.dumps(report,indent=2))
asyncio.run(main())
