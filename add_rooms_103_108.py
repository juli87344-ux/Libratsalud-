from pathlib import Path
p=Path("index.html")
s=p.read_text(encoding="utf-8")

marker='async function cargar(){try{const r=await fetch(SUPABASE_URL+"/rest/v1/camas?select=*&order=habitacion,cama",{headers});if(!r.ok)throw new Error(await r.text());camas=await r.json();const st=document.getElementById("status");st.className="status connection-ok";st.textContent="● Sistema conectado · "+camas.length+" camas · Actualizado "+new Date().toLocaleTimeString("es-AR",{hour:"2-digit",minute:"2-digit"});render()}catch(e){const st=document.getElementById("status");st.className="status connection-bad";st.textContent="● Sin conexión · se reintentará automáticamente";console.error(e)}}'

replacement='''async function asegurarCamasNuevas(actuales){
 const requeridas=[];
 for(let h=103;h<=108;h++)for(const cama of ["A","B"])requeridas.push({habitacion:String(h),cama});
 const faltantes=requeridas.filter(n=>!actuales.some(c=>String(c.habitacion)===n.habitacion&&String(c.cama).toUpperCase()===n.cama));
 if(!faltantes.length)return false;
 const now=new Date().toISOString();
 const nuevas=faltantes.map(x=>({...x,estado:"ocupada",estado_desde:now,actualizado:now,operador_estado:"Sistema",responsable:"Sistema"}));
 try{
  const r=await fetch(SUPABASE_URL+"/rest/v1/camas",{method:"POST",headers:{...headers,"Prefer":"return=minimal"},body:JSON.stringify(nuevas)});
  if(!r.ok){console.error("No se pudieron agregar las nuevas camas",await r.text());return false}
  return true;
 }catch(e){console.error("No se pudieron agregar las nuevas camas",e);return false}
}
async function cargar(){try{let r=await fetch(SUPABASE_URL+"/rest/v1/camas?select=*&order=habitacion,cama",{headers});if(!r.ok)throw new Error(await r.text());camas=await r.json();if(await asegurarCamasNuevas(camas)){r=await fetch(SUPABASE_URL+"/rest/v1/camas?select=*&order=habitacion,cama",{headers});if(r.ok)camas=await r.json()}const st=document.getElementById("status");st.className="status connection-ok";st.textContent="● Sistema conectado · "+camas.length+" camas · Actualizado "+new Date().toLocaleTimeString("es-AR",{hour:"2-digit",minute:"2-digit"});render()}catch(e){const st=document.getElementById("status");st.className="status connection-bad";st.textContent="● Sin conexión · se reintentará automáticamente";console.error(e)}}'''

if marker not in s:
    raise SystemExit("No se encontró cargar() esperado")
s=s.replace(marker,replacement)
p.write_text(s,encoding="utf-8")
# ejecutar
