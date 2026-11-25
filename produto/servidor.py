"""Servidor HTTP. Uso: python servidor.py [porta]

A senha da coordenação vem da variável SENHA_COORDENACAO; sem ela, uma senha nova é
sorteada e mostrada no terminal a cada início.
"""
import base64
import binascii
import os
import secrets
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import banco
import paginas
import servico as s

LIMITE_CORPO = 64 * 1024


def inteiro(texto):
    try:
        return int(texto)
    except ValueError:
        raise s.ErroRegra("Identificador inválido.")


class Pedido(BaseHTTPRequestHandler):
    senha = None
    arquivo = banco.ARQUIVO

    def do_GET(self):
        self.atender({
            "/": self.ver_inicio, "/minha": self.ver_minha,
            "/certificado": self.ver_certificado, "/validar": self.ver_validar,
            "/coordenacao": self.ver_coordenacao, "/coordenacao/chamada": self.ver_chamada,
        }, parse_qs(urlsplit(self.path).query))

    def do_POST(self):
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            tamanho = -1
        if not 0 <= tamanho <= LIMITE_CORPO:
            return self.responder(413, paginas.erro("Pedido grande demais."))
        corpo = self.rfile.read(tamanho).decode("utf-8", "replace")
        # Outro site não pode enviar formulários em nome de quem está logado.
        origem = self.headers.get("Origin")
        if origem and urlsplit(origem).netloc != self.headers.get("Host"):
            return self.responder(403, paginas.erro("Origem não permitida."))
        self.atender({
            "/inscrever": self.fazer_inscricao, "/coordenacao/atividade": self.fazer_atividade,
            "/coordenacao/chamada": self.fazer_chamada, "/coordenacao/encerrar": self.fazer_encerrar,
        }, parse_qs(corpo))

    def atender(self, rotas, campos):
        caminho = urlsplit(self.path).path
        acao = rotas.get(caminho)
        if acao is None:
            return self.responder(404, paginas.erro("Página não encontrada."))
        if caminho.startswith("/coordenacao") and not self.autorizado():
            return self.responder(401, paginas.erro("Área da coordenação."),
                                  {"WWW-Authenticate": 'Basic realm="Coordenacao", charset="UTF-8"'})
        self.campos = campos
        self.con = banco.conectar(self.arquivo)
        try:
            acao()
        except s.ErroRegra as erro:
            self.responder(400, paginas.erro(str(erro)))
        finally:
            self.con.close()

    def autorizado(self):
        tipo, _, dado = self.headers.get("Authorization", "").partition(" ")
        if tipo != "Basic":
            return False
        try:
            senha = base64.b64decode(dado, validate=True).partition(b":")[2]
        except (binascii.Error, ValueError):
            return False
        return secrets.compare_digest(senha, self.senha.encode())

    def campo(self, nome):
        return self.campos.get(nome, [""])[0]

    def responder(self, status, html, extras=None):
        dados = html.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Referrer-Policy", "no-referrer" if status == 200 else "same-origin")
        for nome, valor in (extras or {}).items():
            self.send_header(nome, valor)
        self.end_headers()
        self.wfile.write(dados)

    def ir_para(self, destino):
        self.send_response(303)
        self.send_header("Location", destino)
        self.send_header("Content-Length", "0")
        self.end_headers()

    # --- público ---
    def ver_inicio(self):
        self.responder(200, paginas.inicio(s.listar_atividades(self.con), s.encerrado(self.con)))

    def fazer_inscricao(self):
        ids = [inteiro(x) for x in self.campos.get("atividade", [])]
        codigo = s.inscrever(self.con, self.campo("nome"), self.campo("email"), ids)
        self.ir_para(f"/minha?c={codigo}")

    def ver_minha(self):
        pessoa = s.pessoa_por_codigo(self.con, self.campo("c"))
        if pessoa is None:
            raise s.ErroRegra("Inscrição não encontrada.")
        self.responder(200, paginas.minha(
            pessoa, s.inscricoes_da_pessoa(self.con, pessoa["id"]), s.encerrado(self.con)))

    def ver_certificado(self):
        self.responder(200, paginas.certificado(s.emitir_certificado(self.con, self.campo("c"))))

    def ver_validar(self):
        codigo = self.campo("codigo")
        self.responder(200, paginas.validar(codigo, s.validar(self.con, codigo)))

    # --- coordenação ---
    def ver_coordenacao(self):
        self.responder(200, paginas.coordenacao(s.listar_atividades(self.con), s.encerrado(self.con)))

    def fazer_atividade(self):
        s.criar_atividade(self.con, *(self.campo(c) for c in ("titulo", "inicio", "fim", "vagas")))
        self.ir_para("/coordenacao")

    def ver_chamada(self):
        numero = inteiro(self.campo("id"))
        atividade = next((a for a in s.listar_atividades(self.con) if a["id"] == numero), None)
        if atividade is None:
            raise s.ErroRegra("Atividade inexistente.")
        self.responder(200, paginas.chamada(
            atividade, s.lista_de_chamada(self.con, numero), s.encerrado(self.con)))

    def fazer_chamada(self):
        numero = inteiro(self.campo("id"))
        s.gravar_chamada(self.con, numero, [inteiro(x) for x in self.campos.get("presente", [])])
        self.ir_para(f"/coordenacao/chamada?id={numero}")

    def fazer_encerrar(self):
        s.encerrar(self.con)
        self.ir_para("/coordenacao")


def main():
    porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    Pedido.senha = os.environ.get("SENHA_COORDENACAO") or secrets.token_urlsafe(9)
    if not os.environ.get("SENHA_COORDENACAO"):
        print(f"Senha da coordenação (usuário: qualquer): {Pedido.senha}", flush=True)
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), Pedido)
    print(f"http://127.0.0.1:{porta}", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
