"""Package the buildless template, source helpers, documentation and small QA reports."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
archive=ROOT/'oculis-optical-store-template.zip'
with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=8) as z:
 for file in sorted(ROOT.rglob('*')):
  if not file.is_file() or file==archive:continue
  rel=file.relative_to(ROOT)
  if any(part in {'.git','__pycache__','.DS_Store'} for part in rel.parts):continue
  if rel.parts[:2]==('tests','artifacts') and file.suffix not in {'.json'}:continue
  z.write(file,Path('oculis-optical-store-template')/rel)
with ZipFile(archive) as z:
 assert z.testzip() is None
 names=z.namelist()
 for page in ['index.html','home-2.html','about.html','products.html','product-details.html','eye-test-booking.html','brands.html','services.html','service-details.html','blog.html','blog-details.html','contact.html','404.html','coming-soon.html']:
  assert 'oculis-optical-store-template/'+'pages/'+page in names
 print('Verified archive:',archive.name,'—',len(names),'files —',round(archive.stat().st_size/1024/1024,2),'MiB')
