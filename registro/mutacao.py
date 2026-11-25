"""Estraga uma linha por vez, numa cópia do produto, e vê se os testes percebem.

Uso: python registro/mutacao.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PRODUTO = Path(__file__).resolve().parent.parent / "produto"
MUTACOES = [
    ("servico.py", "feitos >= total * MINIMO_PRESENCA", "feitos > total * MINIMO_PRESENCA"),
    ("servico.py", 'a["inicio"] < b["fim"]', 'a["inicio"] <= b["fim"]'),
    ("servico.py", 'b["inicio"] < a["fim"]', 'b["inicio"] <= a["fim"]'),
    ("servico.py", 'a["livres"] < 1', 'a["livres"] < 0'),
    ("servico.py", "BEGIN IMMEDIATE", "BEGIN"),
    ("servico.py", "email.strip().lower()", "email.strip()"),
    ("servico.py", "if x[\"presente\"])", ")"),
    ("servico.py", "    ids = set(ids)\n", "    ids = list(ids)\n"),
    ("servico.py", "if not presentes <= inscritos", "if False"),
    ("servico.py", "validacao.strip().upper()", "validacao.strip()"),
    ("servico.py", "if validacao is None", "if True"),
    ("servico.py", "    with transacao(con):\n        exigir_aberto(con)\n        return con", "    with transacao(con):\n        return con"),
    ("servidor.py", 'startswith("/coordenacao")', 'startswith("/coordenacao/")'),
    ("servidor.py", "if origem and", "if False and"),
    ("paginas.py", '{e(a["titulo"])} — ', '{a["titulo"]} — '),
    ("paginas.py", '<h2>{e(c["nome"])}</h2>', '<h2>{c["nome"]}</h2>'),
]

escaparam = 0
for n, (arquivo, antes, depois) in enumerate(MUTACOES, 1):
    with tempfile.TemporaryDirectory() as pasta:
        copia = Path(pasta) / "p"
        shutil.copytree(PRODUTO, copia, ignore=shutil.ignore_patterns("__pycache__", "*.db"))
        alvo = copia / arquivo
        texto = alvo.read_text(encoding="utf-8")
        assert texto.count(antes) >= 1, (arquivo, antes)
        alvo.write_text(texto.replace(antes, depois, 1), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=copia, capture_output=True, timeout=120)
    pegou = r.returncode != 0
    escaparam += not pegou
    print(f"{n:2} {'pega   ' if pegou else 'ESCAPOU'} {arquivo}: {antes.strip().splitlines()[0]!r}")
print(f"{len(MUTACOES) - escaparam} de {len(MUTACOES)} percebidas")
