#!/usr/bin/env python3
"""Confere links locais, âncoras e imagens nas páginas publicadas."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, file):
        super().__init__()
        self.file, self.ids, self.refs, self.errors = file, set(), [], []
        self.h1 = 0
        self.feed(file.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f'ID repetido: {attrs["id"]}')
            self.ids.add(attrs['id'])
        self.h1 += tag == 'h1'
        for attribute in ('src', 'href'):
            if attrs.get(attribute):
                self.refs.append(attrs[attribute])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('Imagem sem atributo alt')

pages = {file.resolve(): Page(file) for file in [ROOT / 'index.html', *sorted((ROOT / 'projetos').glob('*.html'))]}
errors, count = [], 0
for path, page in pages.items():
    errors.extend(f'{path.name}: {e}' for e in page.errors)
    if page.h1 != 1:
        errors.append(f'{path.name}: esperado um h1; encontrados {page.h1}')
    for ref in page.refs:
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc:
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        count += 1
        if not target.is_file():
            errors.append(f'{path.name}: arquivo ausente {ref}')
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: âncora ausente {ref}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'OK: {len(pages)} páginas, {count} referências locais, âncoras e textos alternativos.')
