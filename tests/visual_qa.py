"""Chrome QA: every required width, both themes and both directions; meaningful interaction checks."""
import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/artifacts';OUT.mkdir(parents=True,exist_ok=True)
MANIFEST=json.loads((ROOT/'scripts/page-manifest.json').read_text())
WIDTHS=[320,360,375,390,420,480,640,768,820,1024,1280,1440,1920]
BASE='http://127.0.0.1:8765/'
async def main():
 report={'browser':'Google Chrome via Playwright','widths':WIDTHS,'pages':{},'failures':[],'interactions':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
  context=await browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light',reduced_motion='reduce')
  page=await context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  for file,meta in MANIFEST.items():
   await page.goto(BASE+("pages/"+file));await page.evaluate('document.fonts.ready')
   # Load every lazy image before auditing.
   await page.evaluate("""async()=>{const images=[...document.images];images.forEach(i=>i.loading='eager');await Promise.all(images.map(i=>i.decode().catch(()=>{})))}""")
   count=await page.locator('main > section').count()
   if count!=meta['sections']:report['failures'].append([file,'sections',count])
   broken=await page.evaluate("[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src'))")
   if broken:report['failures'].append([file,'broken-images',broken])
   checks=0
   for theme,direction in [('light','ltr'),('dark','ltr'),('light','rtl'),('dark','rtl')]:
    await page.evaluate('([t,d])=>{document.documentElement.dataset.theme=t;document.documentElement.dir=d}',[theme,direction])
    for width in WIDTHS:
     await page.set_viewport_size({'width':width,'height':1000 if width>640 else 844})
     measurements=await page.evaluate("""()=>{let w=document.documentElement.clientWidth;return {overflow:document.documentElement.scrollWidth-w, offenders:[...document.querySelectorAll('main *,header *,footer *')].filter(e=>{let r=e.getBoundingClientRect();return r.width&& (r.right>w+1||r.left< -1)}).slice(0,8).map(e=>e.tagName+'.'+e.className)}}""")
     if measurements['overflow']>1:report['failures'].append([file,theme,direction,width,measurements])
     checks+=1
     if (theme,direction)==('light','ltr') and width in [390,820,1440] or (theme,direction)==('dark','rtl') and width in [390,1440]:
      height=await page.evaluate('document.documentElement.scrollHeight');await page.set_viewport_size({'width':width,'height':height});await page.wait_for_timeout(180);await page.screenshot(path=str(OUT/f'{file[:-5]}-{width}-{theme}-{direction}.png'));await page.set_viewport_size({'width':width,'height':1000 if width>640 else 844})
   report['pages'][file]={'sections':count,'layout_checks':checks,'broken_images':broken}
   print(file,checks,'layout checks',flush=True)
  async def test(name,action):
   try:await action();report['interactions'].append({'name':name,'passed':True})
   except Exception as e:report['failures'].append(['interaction',name,str(e)]);report['interactions'].append({'name':name,'passed':False})
  async def catalogue():
   await page.set_viewport_size({'width':1440,'height':1000});await page.goto(BASE+'pages/products.html')
   await page.locator('#product-search').fill('zzznomatch');assert await page.locator('#product-empty').is_visible()
   await page.locator('#reset-products').click();assert await page.locator('#product-count').inner_text()=='12 frames'
   await page.locator('#filter-style').select_option('Round');assert await page.locator('#product-count').inner_text()=='3 frames'
   await page.locator('#filter-category').select_option('Sunglasses');assert await page.locator('#product-count').inner_text()=='1 frame'
   await page.locator('#reset-products').click();await page.locator('#product-sort').select_option('price-desc');assert await page.locator('#product-grid .product-card').first.get_attribute('data-id')=='arlo'
   await page.locator('#filter-lens').select_option('Reading');assert await page.locator('#product-count').inner_text()=='3 frames'
   await page.locator('[data-preset="Square"]').click();assert await page.locator('#product-count').inner_text()=='1 frame'
  await test('Catalogue search, category/style/lens intersection, sorting, empty state and preset chips',catalogue)
  async def preference():
   await page.goto(BASE+'pages/index.html');await page.locator('#theme-toggle').click();await page.locator('#rtl-toggle').click();await page.goto(BASE+'pages/about.html');assert await page.evaluate('document.documentElement.dataset.theme')=='dark';assert await page.evaluate('document.documentElement.dir')=='rtl';await page.locator('#theme-toggle').click();await page.locator('#rtl-toggle').click()
  await test('Theme and RTL persist across page navigation',preference)
  async def navigation():
   await page.set_viewport_size({'width':1440,'height':1000});await page.goto(BASE+'pages/index.html');await page.locator('.nav-home').focus();await page.keyboard.press('ArrowDown');assert await page.locator('#home-menu').is_visible();await page.keyboard.press('Escape');assert not await page.locator('#home-menu').is_visible()
   await page.set_viewport_size({'width':390,'height':844});await page.locator('#menu-toggle').click();assert await page.locator('#primary-nav').is_visible();await page.locator('.nav-home').click();await page.locator('#home-menu a').nth(1).click();assert 'home-2.html' in page.url;await page.locator('#menu-toggle').click();await page.keyboard.press('Escape');assert not await page.locator('#primary-nav').is_visible()
  await test('Desktop keyboard dropdown and touch-size mobile navigation',navigation)
  async def gallery():
   await page.goto(BASE+'pages/product-details.html');await page.locator('.gallery-thumb').nth(1).click();assert 'detail-side' in await page.locator('.gallery-main img').get_attribute('src');await page.goto(BASE+'pages/product-details.html?id=ellis');assert await page.locator('#detail-name').inner_text()=='The Ellis'
  await test('Product gallery and product-specific detail routes',gallery)
  async def brands():
   await page.goto(BASE+'pages/brands.html');await page.locator('#brand-search').fill('zzznomatch');assert await page.locator('#brand-empty').is_visible();await page.locator('#brand-search').fill('');await page.locator('#brand-filter').select_option('Metal');assert await page.locator('#brand-count').inner_text()=='2 labels'
  await test('Brand search, material filter and empty results',brands)
  async def blog():
   await page.goto(BASE+'pages/blog.html');assert await page.locator('#blog-grid .article-card:visible').count()==3;await page.locator('#blog-more').click();assert await page.locator('#blog-grid .article-card:visible').count()==5;await page.locator('[data-blog-category="Lens guides"]').click();assert await page.locator('#blog-grid .article-card:visible').count()==2;await page.locator('#blog-search').fill('zzznomatch');assert await page.locator('#blog-empty').is_visible()
   await page.goto(BASE+'pages/blog-details.html?id=screen-breaks');assert 'screen break' in (await page.locator('#article-title').inner_text()).lower()
  await test('Journal search, categories, load-more and article routes',blog)
  async def booking():
   await page.goto(BASE+'pages/eye-test-booking.html');await page.locator('button[type=submit]').click();assert await page.locator('[aria-invalid=true]').count()>=6
   await page.locator('#service').select_option(index=1);await page.locator('#date').fill('2020-01-01');await page.locator('#time').select_option(index=1);await page.locator('#name').fill('Demo User');await page.locator('#email').fill('demo@example.com');await page.locator('#phone').fill('9876543210');await page.locator('button[type=submit]').click();assert 'future' in await page.locator('#date-error').inner_text()
   today=await page.locator('#date').get_attribute('min');await page.locator('#date').fill(today);await page.locator('button[type=submit]').click();assert 'No appointment has been booked' in await page.locator('.form-status').inner_text();assert await page.locator('#email').input_value()==''
  await test('Booking required fields, past-date prevention and demo confirmation',booking)
  async def contact():
   await page.goto(BASE+'pages/contact.html');await page.locator('#name').fill('Demo User');await page.locator('#email').fill('bad');await page.locator('#subject').select_option(index=1);await page.locator('#message').fill('A demo product enquiry.');await page.locator('button[type=submit]').click();assert await page.locator('#email-error').inner_text();await page.locator('#email').fill('demo@example.com');await page.locator('button[type=submit]').click();assert 'not been sent or stored' in await page.locator('.form-status').inner_text()
  await test('Contact email validation and explicit demo feedback',contact)
  async def newsletter():
   await page.goto(BASE+'pages/coming-soon.html');await page.locator('#launch-email').fill('bad');await page.locator('button[type=submit]').click();assert await page.locator('#launch-email-error').inner_text();await page.locator('#launch-email').fill('demo@example.com');await page.locator('button[type=submit]').click();assert 'not been stored or sent' in await page.locator('.form-status').inner_text()
  await test('Newsletter validation and demo confirmation',newsletter)
  async def testimonials():
   await page.set_viewport_size({'width':390,'height':844});await page.goto(BASE+'pages/index.html');assert await page.locator('#testimonials .quote-card:visible').count()==1;await page.locator('#testimonial-next').click();assert await page.locator('#testimonial-status').inner_text()=='Story 2 of 4';await page.locator('#testimonial-prev').click();assert await page.locator('#testimonial-status').inner_text()=='Story 1 of 4'
  await test('Manual testimonial carousel and mobile single-story view',testimonials)
  async def accordion():
   await page.goto(BASE+'pages/service-details.html');await page.locator('summary').first.focus();await page.keyboard.press('Enter');assert await page.locator('details').first.get_attribute('open') is not None
  await test('Keyboard accessible FAQ accordion',accordion)
  report['javascript_errors']=errors
  if errors:report['failures'].append(['javascript',errors])
  await browser.close()
 (OUT/'qa-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'layout_checks':sum(v['layout_checks'] for v in report['pages'].values()),'failures':report['failures'],'interactions':report['interactions']},indent=2))
 if report['failures']:sys.exit(1)
asyncio.run(main())
