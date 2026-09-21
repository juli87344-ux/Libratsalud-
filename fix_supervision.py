from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")
s = s.replace("+\\n  ", "+\n  ")
p.write_text(s, encoding="utf-8")
# trigger
