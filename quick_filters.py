from pathlib import Path

p=Path("index.html")
s=p.read_text(encoding="utf-8")

s=s.replace(
'.quickstat{background:#fff;border:1px solid #d9e8f0;border-radius:13px;padding:9px 8px;min-height:66px;box-shadow:0 3px 12px rgba(23,70,100,.045);display:flex;flex-direction:column;justify-content:center}',
'.quickstat{background:#fff;border:1px solid #d9e8f0;border-radius:13px;padding:9px 8px;min-height:66px;box-shadow:0 3px 12px rgba(23,70,100,.045);display:flex;flex-direction:column;justify-content:center;text-align:left;cursor:pointer;width:100%}.quickstat:active{transform:scale(.985)}'
)

s=s.replace(
'''  '<div class="quickstat ocupadas"><span>Ocupadas</span><b>'+(counts.ocupada||0)+'</b></div>'+ 
  '<div class="quickstat altas"><span>Alta / traslado</span><b>'+(counts.alta_espera||0)+'</b></div>'+ 
  '<div class="quickstat limpiar"><span>Por limpiar</span><b>'+((counts.liberada||0)+(counts.en_limpieza||0))+'</b></div>'+ 
  '<div class="quickstat libres"><span>Libres listas</span><b>'+(counts.lista||0)+'</b></div>';''',
'''  '<button class="quickstat ocupadas" onclick="setQuickFilter(\'ocupada\')"><span>Ocupadas</span><b>'+(counts.ocupada||0)+'</b></button>'+ 
  '<button class="quickstat altas" onclick="setQuickFilter(\'alta_espera\')"><span>Alta / traslado</span><b>'+(counts.alta_espera||0)+'</b></button>'+ 
  '<button class="quickstat limpiar" onclick="setQuickFilter(\'por_limpiar\')"><span>Por limpiar</span><b>'+((counts.liberada||0)+(counts.en_limpieza||0))+'</b></button>'+ 
  '<button class="quickstat libres" onclick="setQuickFilter(\'lista\')"><span>Libres listas</span><b>'+(counts.lista||0)+'</b></button>';'''
)

marker='function setFilter(v){filtro=v;localStorage.setItem("libratsalud_filtro",v);renderFilters();render()}'
replacement='''function setFilter(v){filtro=v;localStorage.setItem("libratsalud_filtro",v);renderFilters();render()}
function setQuickFilter(v){filtro=v;localStorage.setItem("libratsalud_filtro",v);renderFilters();render();document.getElementById("rooms")?.scrollIntoView({behavior:"smooth",block:"start"});}'''
if marker in s and 'function setQuickFilter' not in s:
    s=s.replace(marker,replacement)

s=s.replace(
'let data=filtro==="todas"?[...camas]:camas.filter(c=>c.estado===filtro);',
'let data=filtro==="todas"?[...camas]:filtro==="por_limpiar"?camas.filter(c=>c.estado==="liberada"||c.estado==="en_limpieza"):camas.filter(c=>c.estado===filtro);'
)

s=s.replace(
'const f=[["todas","Todas",camas.length],...Object.entries(STATES).map(([k,v])=>[k,v[0],counts[k]||0])];',
'const f=[["todas","Todas",camas.length],["por_limpiar","Por limpiar",(counts.liberada||0)+(counts.en_limpieza||0)],...Object.entries(STATES).map(([k,v])=>[k,v[0],counts[k]||0])];'
)

p.write_text(s,encoding="utf-8")
# ejecutar
