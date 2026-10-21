// Valida la lógica de agregación del dashboard v2 con los datos reales (data/bajas.json)
import fs from "node:fs";

const RAW = JSON.parse(fs.readFileSync(new URL("../data/bajas.json", import.meta.url)));
const yearOf = d => d.slice(0, 4);

// KPIs
const totalUnits = RAW.reduce((s, r) => s + r.qty, 0);
const totalLines = RAW.length;
const docs = new Set(RAW.map(r => r.doc)).size;
const u25 = RAW.filter(r => yearOf(r.date) === "2025").reduce((s, r) => s + r.qty, 0);
const u26 = RAW.filter(r => yearOf(r.date) === "2026").reduce((s, r) => s + r.qty, 0);
const varPct = Math.round((u26 - u25) / u25 * 100);

// Trazabilidad
const sinSerial = RAW.filter(r => !r.serie || /^(n\/n|ng|na)$/i.test((r.serie || "").trim())).length;
const sinInv = RAW.filter(r => !r.inv || /^(sin c|ng|na|n\/n)/i.test((r.inv || "").trim())).length;
const lotes = RAW.filter(r => r.qty > 1).length;

// Categorías
const byCat = {};
RAW.forEach(r => byCat[r.cat] = (byCat[r.cat] || 0) + r.qty);
const topCats = Object.entries(byCat).sort((a, b) => b[1] - a[1]).slice(0, 5);

// Marcas
const byBrand = {};
RAW.forEach(r => byBrand[r.brand] = (byBrand[r.brand] || 0) + r.qty);
const topBrands = Object.entries(byBrand).sort((a, b) => b[1] - a[1]).slice(0, 5);

console.log("=== VALIDACIÓN LÓGICA DASHBOARD v2 ===");
console.log("Registros (líneas):", totalLines);
console.log("Unidades totales  :", totalUnits);
console.log("Documentos (DITI) :", docs);
console.log("Unidades 2025     :", u25);
console.log("Unidades 2026     :", u26);
console.log("Variación % 25→26 :", varPct + "%");
console.log("Sin serial        :", sinSerial, `(${Math.round(sinSerial/totalLines*100)}%)`);
console.log("Sin inventario    :", sinInv, `(${Math.round(sinInv/totalLines*100)}%)`);
console.log("Líneas tipo lote  :", lotes, `(${Math.round(lotes/totalLines*100)}%)`);
console.log("Top categorías    :", topCats.map(c => `${c[0]}=${c[1]}`).join(", "));
console.log("Top marcas        :", topBrands.map(b => `${b[0]}=${b[1]}`).join(", "));

// Comprobaciones duras
const errs = [];
if (totalLines !== 935) errs.push("totalLines != 935");
if (u25 + u26 !== totalUnits) errs.push("u25+u26 != totalUnits (hay fechas fuera de 2025/2026)");
if (byCat["Monitor"] === undefined) errs.push("falta categoría Monitor");
// Verificar que la corrección de categoría funcionó: ningún "Teléfono ... pantalla" debe ser Monitor
const malClasif = RAW.filter(r => r.cat === "Monitor" && /tel[eé]fono|avaya/i.test(r.desc));
if (malClasif.length) errs.push(`${malClasif.length} teléfonos siguen como Monitor`);

console.log("\n=== RESULTADO ===");
console.log(errs.length ? "❌ FALLOS: " + errs.join("; ") : "✅ Todas las comprobaciones OK");
