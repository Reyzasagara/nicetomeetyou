"""Validate generated portfolio pages and their local links (standard library only)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re
ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.ids=set(); self.links=[]; self.h1=0
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs['id'])
        self.h1 += tag == 'h1'
        for key in ('href','src'):
            if key in attrs:self.links.append(attrs[key])
files=[ROOT / name for name in ['index.html','work.html','cv.html','lab.html','powersync.html']]
files+=list(ROOT.glob('domain-*.html'))+list(ROOT.glob('work-*.html'))
files += [ROOT/'id'/p.name for p in files.copy()]
docs={p:Document(p) for p in files}
for p,doc in docs.items():
    assert doc.h1==1, f'{p.name}: expected one H1'
    for link in doc.links:
        url=urlsplit(link)
        if url.scheme or url.netloc: continue
        dest=(p.parent/unquote(url.path)).resolve() if url.path else p
        assert dest.exists(),f'{p.name}: missing {link}'
        if url.fragment and dest.suffix=='.html':
            target=docs.get(dest) or Document(dest)
            assert unquote(url.fragment) in target.ids,f'{p.name}: missing anchor {link}'
    text=p.read_text(encoding='utf-8')
    emails=set(re.findall(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',text))
    assert emails <= {'reyzacomm@gmail.com'},f'{p.name}: unexpected email {emails}'
    assert not re.search(r'https?://(?:localhost|127\.0\.0\.1|10\.\d+\.|192\.168\.)',text),p
    assert not any(x in text for x in ['debug mode on','unsafe upload path','serious security problems']),p
for language in ('','id'):
    text=(ROOT/language/'index.html').read_text(encoding='utf-8')
    assert text.count('<article class="project-card')==3
    assert text.index('id="work"')<text.index('id="domains"')
    assert 'work.html' in text
print(f'PASS: {len(files)} pages; local files and anchors, heading IDs, homepage order, contact allowlist and disclosure regression checks.')
