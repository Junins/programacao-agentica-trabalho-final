"""Regras da semana acadêmica. Nada aqui sabe de HTTP ou HTML."""
import re
import secrets
from contextlib import contextmanager
from datetime import datetime

MINIMO_PRESENCA = 0.75


class ErroRegra(Exception):
    """Pedido recusado por uma regra; a mensagem pode ser mostrada à pessoa."""


@contextmanager
def transacao(con):
    con.execute("BEGIN IMMEDIATE")
    try:
        yield
    except BaseException:
        con.execute("ROLLBACK")
        raise
    con.execute("COMMIT")


def encerrado(con):
    return bool(con.execute("SELECT encerrado FROM evento").fetchone()[0])


def exigir_aberto(con):
    if encerrado(con):
        raise ErroRegra("O evento já foi encerrado.")


def minutos(atividade):
    inicio = datetime.fromisoformat(atividade["inicio"])
    fim = datetime.fromisoformat(atividade["fim"])
    return int((fim - inicio).total_seconds() // 60)


def criar_atividade(con, titulo, inicio, fim, vagas):
    titulo = titulo.strip()
    if not titulo:
        raise ErroRegra("Informe o título da atividade.")
    try:
        d_inicio, d_fim = datetime.fromisoformat(inicio), datetime.fromisoformat(fim)
        vagas = int(vagas)
    except ValueError:
        raise ErroRegra("Data ou número de vagas inválido.")
    if d_inicio.tzinfo or d_fim.tzinfo:
        raise ErroRegra("Data ou número de vagas inválido.")
    if d_fim <= d_inicio:
        raise ErroRegra("O fim precisa ser depois do início.")
    if vagas < 1:
        raise ErroRegra("A atividade precisa de ao menos uma vaga.")
    formato = "%Y-%m-%dT%H:%M"
    with transacao(con):
        exigir_aberto(con)
        return con.execute(
            "INSERT INTO atividade (titulo, inicio, fim, vagas) VALUES (?, ?, ?, ?)",
            (titulo, d_inicio.strftime(formato), d_fim.strftime(formato), vagas),
        ).lastrowid


def listar_atividades(con):
    return con.execute(
        """SELECT a.*, a.vagas - COUNT(i.pessoa_id) AS livres
           FROM atividade a LEFT JOIN inscricao i ON i.atividade_id = a.id
           GROUP BY a.id ORDER BY a.inicio, a.id"""
    ).fetchall()


def conflitam(a, b):
    return a["inicio"] < b["fim"] and b["inicio"] < a["fim"]


def inscrever(con, nome, email, ids):
    """Inscreve tudo ou nada. Devolve o código do link pessoal."""
    nome = " ".join(nome.split())
    email = email.strip().lower()
    if not nome:
        raise ErroRegra("Informe o nome.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ErroRegra("Informe um e-mail válido.")
    ids = set(ids)
    if not ids:
        raise ErroRegra("Escolha ao menos uma atividade.")
    with transacao(con):
        exigir_aberto(con)
        if con.execute("SELECT 1 FROM pessoa WHERE email = ?", (email,)).fetchone():
            raise ErroRegra("Este e-mail já tem inscrição.")
        escolhidas = [a for a in listar_atividades(con) if a["id"] in ids]
        if len(escolhidas) != len(ids):
            raise ErroRegra("Atividade inexistente.")
        for n, a in enumerate(escolhidas):
            if a["livres"] < 1:
                raise ErroRegra(f"Não há vaga em: {a['titulo']}.")
            for b in escolhidas[n + 1:]:
                if conflitam(a, b):
                    raise ErroRegra(
                        f"Horários em conflito: {a['titulo']} e {b['titulo']}.")
        codigo = secrets.token_urlsafe(16)
        pessoa_id = con.execute(
            "INSERT INTO pessoa (nome, email, codigo) VALUES (?, ?, ?)",
            (nome, email, codigo)).lastrowid
        con.executemany(
            "INSERT INTO inscricao (pessoa_id, atividade_id) VALUES (?, ?)",
            [(pessoa_id, a["id"]) for a in escolhidas])
    return codigo


def pessoa_por_codigo(con, codigo):
    return con.execute("SELECT * FROM pessoa WHERE codigo = ?", (codigo,)).fetchone()


def inscricoes_da_pessoa(con, pessoa_id):
    return con.execute(
        """SELECT a.*, i.presente FROM inscricao i
           JOIN atividade a ON a.id = i.atividade_id
           WHERE i.pessoa_id = ? ORDER BY a.inicio""", (pessoa_id,)).fetchall()


def lista_de_chamada(con, atividade_id):
    return con.execute(
        """SELECT p.id, p.nome, p.email, i.presente FROM inscricao i
           JOIN pessoa p ON p.id = i.pessoa_id
           WHERE i.atividade_id = ? ORDER BY p.nome""", (atividade_id,)).fetchall()


def gravar_chamada(con, atividade_id, ids_presentes):
    """A lista enviada substitui a anterior: quem não vier nela fica ausente."""
    presentes = set(ids_presentes)
    with transacao(con):
        exigir_aberto(con)
        inscritos = {linha["id"] for linha in lista_de_chamada(con, atividade_id)}
        if not presentes <= inscritos:
            raise ErroRegra("Há presença de quem não se inscreveu nesta atividade.")
        con.executemany(
            "UPDATE inscricao SET presente = ? WHERE atividade_id = ? AND pessoa_id = ?",
            [(int(p in presentes), atividade_id, p) for p in inscritos])


def encerrar(con):
    with transacao(con):
        exigir_aberto(con)
        con.execute("UPDATE evento SET encerrado = 1")


def apurar(con, pessoa_id):
    """Minutos inscritos, minutos presentes e se alcança o mínimo."""
    linhas = inscricoes_da_pessoa(con, pessoa_id)
    total = sum(minutos(x) for x in linhas)
    feitos = sum(minutos(x) for x in linhas if x["presente"])
    return total, feitos, total > 0 and feitos >= total * MINIMO_PRESENCA


def emitir_certificado(con, codigo):
    with transacao(con):
        pessoa = pessoa_por_codigo(con, codigo)
        if pessoa is None:
            raise ErroRegra("Inscrição não encontrada.")
        if not encerrado(con):
            raise ErroRegra("O certificado sai depois do encerramento do evento.")
        _, feitos, atingiu = apurar(con, pessoa["id"])
        if not atingiu:
            raise ErroRegra("Presença abaixo de 75% da carga inscrita.")
        validacao = pessoa["certificado"]
        if validacao is None:
            validacao = secrets.token_hex(6).upper()
            con.execute("UPDATE pessoa SET certificado = ? WHERE id = ?",
                        (validacao, pessoa["id"]))
    return {"nome": pessoa["nome"], "minutos": feitos, "validacao": validacao}


def validar(con, validacao):
    pessoa = con.execute("SELECT * FROM pessoa WHERE certificado = ?",
                         (validacao.strip().upper(),)).fetchone()
    if pessoa is None:
        return None
    _, feitos, _ = apurar(con, pessoa["id"])
    return {"nome": pessoa["nome"], "minutos": feitos}
