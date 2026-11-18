import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
  page=await browser.new_page(viewport={'width':1440,'height':1000})
  await page.goto('http://localhost:8765/pages/home-2.html');await page.evaluate('document.fonts.ready')
  await page.evaluate("async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))}")
  print(await page.locator('main>section').evaluate_all('els=>els.map(e=>({heading:e.querySelector("h1,h2").textContent,top:e.offsetTop,height:e.offsetHeight}))'))
  await page.evaluate('scrollTo(0,1500)');await page.wait_for_timeout(300);await page.screenshot(path='tests/artifacts/home2-scroll-inspect.png')
  await page.evaluate('scrollTo(0,0)');height=await page.evaluate('document.documentElement.scrollHeight');await page.set_viewport_size({'width':1440,'height':height});await page.wait_for_timeout(300);await page.screenshot(path='tests/artifacts/home2-tall-inspect.png')
  await browser.close()
asyncio.run(main())
