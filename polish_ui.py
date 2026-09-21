from pathlib import Path

p=Path("index.html")
s=p.read_text(encoding="utf-8")

s=s.replace('</title>\\n<link rel="icon"', '</title>\n<link rel="icon"')

old='<div class="filters" id="filters"></div><div class="status" id="status">Conectando…</div>'
new='<div class="quickstats" id="quickStats"></div><div class="filters" id="filters"></div><div class="status" id="status">Conectando…</div>'
if old in s and 'id="quickStats"' not in s:
    s=s.replace(old,new)

css='''
/* pulido-visual-libracare-v1 */
body{background:linear-gradient(180deg,#f5fbff 0,#edf6fb 100%)}
.top{background:rgba(255,255,255,.96);backdrop-filter:blur(10px);box-shadow:0 3px 16px rgba(20,67,98,.07)}
.logo{color:#0b4774;letter-spacing:-.4px}.logo small{font-weight:700;color:#6a8192;letter-spacing:0}
.content{padding-top:15px}
.toolbar{background:#fff;border:1px solid #dcebf3;border-radius:16px;padding:11px;box-shadow:0 5px 18px rgba(22,75,110,.05)}
.toolbar h1{color:#123f63}
.quickstats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin:9px 0 11px}
.quickstat{background:#fff;border:1px solid #d9e8f0;border-radius:13px;padding:9px 8px;min-height:66px;box-shadow:0 3px 12px rgba(23,70,100,.045);display:flex;flex-direction:column;justify-content:center}
.quickstat span{font-size:9px;font-weight:850;color:#607e92;line-height:1.15}.quickstat b{font-size:22px;line-height:1.05;margin-top:5px;color:#173f5f}
.quickstat.ocupadas{border-top:4px solid #d83a46}.quickstat.altas{border-top:4px solid #8a55c7}.quickstat.limpiar{border-top:4px solid #d8a800}.quickstat.libres{border-top:4px solid #2d9a5f}
.status.connection-ok,.status.connection-bad{background:#fff;border:1px solid #dce9f1;border-radius:999px;padding:7px 10px;width:max-content;max-width:100%;box-shadow:0 2px 8px rgba(20,70,100,.04)}
.room{border-radius:16px;box-shadow:0 5px 16px rgba(24,76,112,.07);transition:transform .14s ease,box-shadow .14s ease}.room:active{transform:scale(.995)}
.bed{transition:transform .12s ease,filter .12s ease}.bed:active{transform:scale(.98);filter:brightness(.98)}
.pill{font-size:9px;letter-spacing:.1px}.timer{font-variant-numeric:tabular-nums}
.bottom{background:rgba(12,54,92,.97);backdrop-filter:blur(10px);box-shadow:0 -4px 16px rgba(5,38,65,.15)}
.bottom button{min-height:48px}.bottom button.active{background:#1687d5;box-shadow:inset 0 0 0 1px rgba(255,255,255,.18)}
@media(max-width:560px){.quickstats{grid-template-columns:repeat(2,1fr)}.quickstat{min-height:58px}.quickstat b{font-size:20px}.toolbar{padding:9px}.content{padding-left:10px;padding-right:10px}}
'''
if '/* pulido-visual-libracare-v1 */' not in s:
    s=s.replace('</style>',css+'\n</style>')

old_fn='''function renderFilters(){
 const counts={};camas.forEach(c=>counts[c.estado]=(counts[c.estado]||0)+1);
 const f=[["todas","Todas",camas.length],...Object.entries(STATES).map(([k,v])=>[k,v[0],counts[k]||0])];
 document.getElementById("filters").innerHTML=f.map(([k,t,n])=>'<button class="filter filter-'+k+' '+(filtro===k?'active':'')+'" onclick="setFilter(\\''+k+'\\')"><span class="filter-dot"></span><span>'+t+'</span><strong>'+n+'</strong></button>').join("");
}'''
new_fn='''function renderFilters(){
 const counts={};camas.forEach(c=>counts[c.estado]=(counts[c.estado]||0)+1);
 const qs=document.getElementById("quickStats");
 if(qs)qs.innerHTML=
  '<div class="quickstat ocupadas"><span>Ocupadas</span><b>'+(counts.ocupada||0)+'</b></div>'+ 
  '<div class="quickstat altas"><span>Alta / traslado</span><b>'+(counts.alta_espera||0)+'</b></div>'+ 
  '<div class="quickstat limpiar"><span>Por limpiar</span><b>'+((counts.liberada||0)+(counts.en_limpieza||0))+'</b></div>'+ 
  '<div class="quickstat libres"><span>Libres listas</span><b>'+(counts.lista||0)+'</b></div>';
 const f=[["todas","Todas",camas.length],...Object.entries(STATES).map(([k,v])=>[k,v[0],counts[k]||0])];
 document.getElementById("filters").innerHTML=f.map(([k,t,n])=>'<button class="filter filter-'+k+' '+(filtro===k?'active':'')+'" onclick="setFilter(\\''+k+'\\')"><span class="filter-dot"></span><span>'+t+'</span><strong>'+n+'</strong></button>').join("");
}'''
if old_fn in s:
    s=s.replace(old_fn,new_fn)
else:
    raise SystemExit("No se encontró renderFilters esperado")

p.write_text(s,encoding="utf-8")
# ejecutar pulido\n