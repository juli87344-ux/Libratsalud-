from pathlib import Path
p=Path("index.html")
s=p.read_text(encoding="utf-8")
s=s.replace('onclick="setQuickFilter(\'ocupada\')"','onclick="setQuickFilter(\\\'ocupada\\\')"')
s=s.replace('onclick="setQuickFilter(\'alta_espera\')"','onclick="setQuickFilter(\\\'alta_espera\\\')"')
s=s.replace('onclick="setQuickFilter(\'por_limpiar\')"','onclick="setQuickFilter(\\\'por_limpiar\\\')"')
s=s.replace('onclick="setQuickFilter(\'lista\')"','onclick="setQuickFilter(\\\'lista\\\')"')
p.write_text(s,encoding="utf-8")
