import json,requests,time
from bs4 import BeautifulSoup
from pathlib import Path
urls=[
'https://www.stsflooring.co.uk/robots.txt',
'https://www.stsflooring.co.uk/sitemap_index.xml',
'https://www.stsflooring.co.uk/wp-sitemap.xml',
'https://www.stsflooring.co.uk/product-category/carpets/',
'https://www.stsflooring.co.uk/product-category/carpets/80-20/',
'https://www.stsflooring.co.uk/product-category/carpets/100-wool/',
'https://www.stsflooring.co.uk/product-category/carpets/polyprop/',
'https://www.stsflooring.com/robots.txt',
'https://www.stsflooring.com/sitemap.xml',
'https://www.stsflooring.com/products1/c-169.html',
'https://www.stsflooring.com/fairisle-4m/c-4518.html']
out=[]
s=requests.Session();s.headers.update({'User-Agent':'Mozilla/5.0 (compatible; ArrisCatalogResearch/1.0)'})
for url in urls:
 try:
  r=s.get(url,timeout=20)
  soup=BeautifulSoup(r.text,'html.parser')
  info={'requested_url':url,'final_url':r.url,'status':r.status_code,'bytes':len(r.content),'title':(soup.title.get_text(' ',strip=True) if soup.title else '')[:250],
        'raw_snippet':r.text[:400] if 'xml' in url or 'txt' in url else '',
        'anchors':[{'text':a.get_text(' ',strip=True)[:85],'href':a.get('href','')} for a in soup.find_all('a',href=True) if ('carpet' in a.get_text(' ',strip=True).lower() or 'carpet' in a.get('href','').lower() or '/c-' in a.get('href',''))][:100]}
 except Exception as e: info={'requested_url':url,'error':str(e)}
 out.append(info); print(url,info.get('status',info.get('error')),'anchors',len(info.get('anchors',[])),flush=True)
 time.sleep(.8)
Path('research/sts').mkdir(parents=True,exist_ok=True)
Path('research/sts/diagnostic.json').write_text(json.dumps(out,indent=2))
