// Valida la lógica del dashboard BI (Entregable 6) con datos reales.
import fs from "node:fs";
const RAW = JSON.parse(fs.readFileSync(new URL("../data/bajas.json", import.meta.url)));
const mk = d => d.slice(0,7), yr = d => d.slice(0,4);

function filtered(state){
  const q=(state.search||"").trim().toLowerCase();
  return RAW.filter(r=>{
    const m=mk(r.date);
    if(state.from && m<state.from) return false;
    if(state.to && m>state.to) return false;
    if(state.year && yr(r.date)!==state.year) return false;
    if(state.cat && r.cat!==state.cat) return false;
    if(state.drillCat && r.cat!==state.drillCat) return false;
    if(state.drillBrand && r.brand!==state.drillBrand) return false;
    if(q){const b=`${r.desc} ${r.serie} ${r.inv} ${r.brand} ${r.cat} ${r.doc}`.toLowerCase();if(!b.includes(q))return false;}
    return true;
  });
}
const errs=[];
// 1. Sin filtros
let d=filtered({});
if(d.length!==935) errs.push("sin filtros != 935: "+d.length);
// 2. Date range (solo 2025-07)
d=filtered({from:"2025-07",to:"2025-07"});
const u=d.reduce((s,r)=>s+r.qty,0);
console.log("Date range 2025-07:",d.length,"registros,",u,"unidades (esperado ~161)");
if(u!==161) errs.push("date range jul-2025 != 161: "+u);
// 3. Drilldown por categoría Mouse
d=filtered({drillCat:"Mouse"});
console.log("Drilldown Mouse:",d.length,"registros,",d.reduce((s,r)=>s+r.qty,0),"unidades");
if(!d.every(r=>r.cat==="Mouse")) errs.push("drillCat no filtra bien");
// 4. Drilldown por marca Dell
d=filtered({drillBrand:"Dell"});
console.log("Drilldown Dell:",d.length,"registros");
if(!d.every(r=>r.brand==="Dell")) errs.push("drillBrand no filtra bien");
// 5. Combinado: año 2026 + date range desde 2026-04
d=filtered({year:"2026",from:"2026-04",to:"2026-12"});
console.log("2026 desde abril:",d.length,"registros,",d.reduce((s,r)=>s+r.qty,0),"unidades");
if(!d.every(r=>yr(r.date)==="2026" && mk(r.date)>="2026-04")) errs.push("combinado falla");
// 6. KPIs globales
const all=filtered({});
const u25=all.filter(r=>yr(r.date)==="2025").reduce((s,r)=>s+r.qty,0);
const u26=all.filter(r=>yr(r.date)==="2026").reduce((s,r)=>s+r.qty,0);
console.log(`KPIs: ${all.reduce((s,r)=>s+r.qty,0)} u. | 2025=${u25} 2026=${u26} var=${Math.round((u26-u25)/u25*100)}%`);

console.log("\n"+(errs.length? "❌ "+errs.join("; ") : "✅ Todas las comprobaciones de lógica OK"));
