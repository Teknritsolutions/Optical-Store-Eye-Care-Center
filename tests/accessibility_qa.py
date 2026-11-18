import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 report={};failures=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
  page=await browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
  for file in json.loads((ROOT/'scripts/page-manifest.json').read_text()):
   await page.goto('http://127.0.0.1:8765/'+("pages/"+file));await page.evaluate('document.fonts.ready');await page.add_script_tag(path='/tmp/optical-axe.min.js')
   for theme,direction in [('light','ltr'),('dark','rtl')]:
    await page.evaluate('([t,d])=>{document.documentElement.dataset.theme=t;document.documentElement.dir=d}',[theme,direction])
    result=await page.evaluate("async()=>{let r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({html:n.html,target:n.target,summary:n.failureSummary}))})),incomplete:r.incomplete.map(v=>v.id)}}")
    report[file+' '+theme+' '+direction]=result
    if result['violations']:failures.append([file,theme,result['violations']])
   print('Accessibility:',file,flush=True)
  await browser.close()
 (ROOT/'tests/artifacts/accessibility-report.json').write_text(json.dumps({'results':report,'failures':failures},indent=2));print(json.dumps(failures,indent=2))
asyncio.run(main())
