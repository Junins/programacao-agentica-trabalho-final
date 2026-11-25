// Usa o produto num Chrome real: inscreve uma pessoa fictícia pelo formulário.
// Uso: node registro/navegador.mjs URL
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const url = process.argv[2], porta = 9333;
const perfil = mkdtempSync(join(tmpdir(), "chrome-"));
const chrome = spawn("C:/Program Files/Google/Chrome/Application/chrome.exe",
  ["--headless=new", `--remote-debugging-port=${porta}`, `--user-data-dir=${perfil}`, "about:blank"], { stdio: "ignore" });
const dormir = ms => new Promise(r => setTimeout(r, ms));
let alvo;
for (let i = 0; i < 40 && !alvo; i++) {
  await dormir(250);
  try { alvo = (await (await fetch(`http://127.0.0.1:${porta}/json`)).json()).find(t => t.type === "page"); } catch {}
}
const ws = new WebSocket(alvo.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let n = 0; const espera = new Map();
ws.onmessage = m => { const d = JSON.parse(m.data); espera.get(d.id)?.(d.result); };
const cdp = (method, params = {}) => new Promise(r => { espera.set(++n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const js = async x => (await cdp("Runtime.evaluate", { expression: x, returnByValue: true })).result.value;
await cdp("Page.navigate", { url }); await dormir(1500);
await js(`document.querySelector('[name=nome]').value='Pessoa Fictícia';
document.querySelector('[name=email]').value='ficticia@exemplo.org';
document.querySelector('[name=atividade]').checked=true; document.querySelector('form').submit()`);
await dormir(1500);
console.log(await js("location.pathname + ' | ' + document.querySelector('h1').innerText + ' | ' + document.body.innerText.slice(0,300)"));
ws.close(); chrome.kill();
