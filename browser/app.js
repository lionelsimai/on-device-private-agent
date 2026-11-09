// On-device demo: WebLLM stub + vanilla-JS TF-IDF offline fallback.
// If WebGPU + @mlc-ai/web-llm are present, a quantized model can be loaded
// (opt-in, one-time download). Otherwise the fallback below runs with no
// download and $0 inference — identical logic to the Python core.
const DOCS = [
  {id:"privacy", title:"Privacy model", text:"This agent runs entirely on device. No query leaves the device, no API key is required, and inference cost is zero."},
  {id:"pricing", title:"Pricing and costs", text:"Inference costs zero dollars because the model runs locally, so 1000 users still cost $0 in inference."},
  {id:"offline", title:"Offline mode", text:"Offline mode works without internet. The index, planner and fallback all run locally."},
  {id:"quantization", title:"Quantization guide", text:"Quantization reduces model size. Q4 GGUF models are roughly 4x smaller than FP16 with a small quality drop."}
];
const STOP = new Set(["the","a","an","and","or","of","to","in","is","are","what","how","do","does","for","on","at","by"]);
const tok = s => s.toLowerCase().match(/[a-z0-9]+/g)?.filter(t => !STOP.has(t) && t.length > 1) || [];
function search(query, k = 2) {
  const q = new Set(tok(query)); let best = [];
  for (const d of DOCS) {
    const dt = tok(d.title + " " + d.text);
    const score = dt.filter(t => q.has(t)).length / Math.sqrt(dt.length || 1);
    if (score > 0) best.push({d, score});
  }
  return best.sort((a,b) => b.score - a.score).slice(0, k);
}
async function tryWebLLM() {
  // Integration stub: returns null unless WebGPU + WebLLM are available.
  if (!navigator.gpu || !window.mlc?.CreateMLCEngine) return null;
  return null; // Wire CreateMLCEngine("Llama-3.2-1B-Instruct-q4f16_1-MLC") here when opting in.
}
let engine = null;
tryWebLLM().then(e => { engine = e;
  document.getElementById("status").textContent = e ? "WebLLM ready (on-device)" : "Offline fallback ready — TF-IDF in your browser, $0 inference, no download.";
});
document.getElementById("ask").onclick = () => {
  const q = document.getElementById("q").value;
  const hits = search(q);
  document.getElementById("out").textContent = hits.length
    ? hits.map(h => h.d.text + "  [" + h.d.id + "]").join("\n") : "No matching local document found.";
};
