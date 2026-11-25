"""HTML. Todo texto vindo de fora passa por e()."""
from html import escape as e

ESTILO = """
body{font:16px/1.5 system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;color:#222}
h1{color:#1e7a2e} table{border-collapse:collapse;width:100%} td,th{border-bottom:1px solid #ddd;padding:.4rem;text-align:left}
label{display:block;margin:.4rem 0} .erro{background:#fde8e8;padding:.6rem} .ok{background:#e8f6ea;padding:.6rem}
button{padding:.5rem 1rem} nav a{margin-right:1rem} .certificado{border:6px double #1e7a2e;padding:3rem;text-align:center}
@media print{nav,.nao-imprimir{display:none}}
"""


def pagina(titulo, corpo):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>{e(titulo)}</title>
<style>{ESTILO}</style></head><body>
<nav><a href="/">Inscrição</a><a href="/validar">Conferir certificado</a><a href="/coordenacao">Coordenação</a></nav>
<h1>{e(titulo)}</h1>{corpo}</body></html>"""


def horas(minutos):
    h, m = divmod(minutos, 60)
    return f"{h}h{m:02d}" if m else f"{h}h"


def quando(a):
    d, h = a["inicio"].split("T")
    ano, mes, dia = d.split("-")
    return f"{dia}/{mes}/{ano} {h} a {a['fim'].replace(d + 'T', '').replace('T', ' ')}"


def erro(mensagem):
    return pagina("Não deu", f'<p class="erro">{e(mensagem)}</p><p><a href="javascript:history.back()">Voltar</a></p>')


def inicio(atividades, encerrado):
    if encerrado:
        return pagina("Semana acadêmica", "<p>Inscrições encerradas.</p>")
    itens = "".join(
        f'<label><input type="checkbox" name="atividade" value="{a["id"]}"{" disabled" if a["livres"] < 1 else ""}> '
        f'{e(a["titulo"])} — {quando(a)} ({a["livres"]} vagas)</label>' for a in atividades)
    return pagina("Semana acadêmica", f"""<form method="post" action="/inscrever">
<label>Nome <input name="nome" required></label>
<label>E-mail <input name="email" type="email" required></label>
{itens or "<p>Nenhuma atividade cadastrada.</p>"}<button>Inscrever</button></form>""")


def minha(pessoa, inscricoes, encerrado):
    linhas = "".join(
        f'<tr><td>{e(i["titulo"])}</td><td>{quando(i)}</td><td>{"presente" if i["presente"] else "—"}</td></tr>'
        for i in inscricoes)
    link = (f'<p><a href="/certificado?c={e(pessoa["codigo"])}">Emitir certificado</a></p>' if encerrado
            else "<p>O certificado aparece aqui depois do encerramento. Guarde este endereço.</p>")
    return pagina(f'Inscrição de {pessoa["nome"]}',
                  f"<table><tr><th>Atividade</th><th>Quando</th><th>Presença</th></tr>{linhas}</table>{link}")


def certificado(c):
    return pagina("Certificado", f"""<div class="certificado"><p>Certificamos que</p><h2>{e(c["nome"])}</h2>
<p>participou da Semana Acadêmica, com carga horária de <b>{horas(c["minutos"])}</b>.</p>
<p>Código de validação: <b>{e(c["validacao"])}</b></p></div>
<p class="nao-imprimir"><button onclick="print()">Imprimir ou salvar em PDF</button></p>""")


def validar(codigo, resultado):
    aviso = ""
    if codigo:
        aviso = (f'<p class="ok">Válido: {e(resultado["nome"])}, {horas(resultado["minutos"])}.</p>'
                 if resultado else '<p class="erro">Código não encontrado.</p>')
    return pagina("Conferir certificado", f"""{aviso}<form><label>Código
<input name="codigo" value="{e(codigo)}"></label><button>Conferir</button></form>""")


def coordenacao(atividades, encerrado):
    linhas = "".join(
        f'<tr><td>{e(a["titulo"])}</td><td>{quando(a)}</td><td>{a["vagas"] - a["livres"]}/{a["vagas"]}</td>'
        f'<td><a href="/coordenacao/chamada?id={a["id"]}">Chamada</a></td></tr>' for a in atividades)
    formularios = "<p>Evento encerrado.</p>" if encerrado else """
<h2>Nova atividade</h2><form method="post" action="/coordenacao/atividade">
<label>Título <input name="titulo" required></label>
<label>Início <input name="inicio" type="datetime-local" required></label>
<label>Fim <input name="fim" type="datetime-local" required></label>
<label>Vagas <input name="vagas" type="number" min="1" required></label><button>Criar</button></form>
<h2>Encerrar</h2><form method="post" action="/coordenacao/encerrar">
<label><input type="checkbox" required> Entendo que não dá para desfazer</label><button>Encerrar o evento</button></form>"""
    return pagina("Coordenação", f"<table><tr><th>Atividade</th><th>Quando</th><th>Inscritos</th><th></th></tr>{linhas}</table>{formularios}")


def chamada(atividade, pessoas, encerrado):
    itens = "".join(
        f'<label><input type="checkbox" name="presente" value="{p["id"]}"{" checked" if p["presente"] else ""}'
        f'{" disabled" if encerrado else ""}> {e(p["nome"])} ({e(p["email"])})</label>' for p in pessoas)
    botao = "" if encerrado else "<button>Gravar chamada</button>"
    return pagina(f'Chamada: {atividade["titulo"]}', f"""<form method="post" action="/coordenacao/chamada">
<input type="hidden" name="id" value="{atividade["id"]}">{itens or "<p>Ninguém inscrito.</p>"}{botao}</form>""")
