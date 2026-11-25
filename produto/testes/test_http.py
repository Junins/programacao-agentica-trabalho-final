"""Sobe o servidor de verdade numa porta livre e conversa com ele por HTTP."""
import base64
import http.client
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlencode

import paginas
import servidor


class Silencioso(servidor.Pedido):
    senha = "senha-só-do-teste"

    def log_message(self, *args):
        pass


class Http(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        Silencioso.arquivo = Path(self.pasta.name) / "t.db"
        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), Silencioso)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.pasta.cleanup()

    def pedir(self, metodo, caminho, campos=None, senha=None, **cabecalhos):
        c = http.client.HTTPConnection(*self.srv.server_address)
        if senha:
            cabecalhos["Authorization"] = "Basic " + base64.b64encode(f"c:{senha}".encode()).decode()
        corpo = urlencode(campos, doseq=True) if campos is not None else None
        c.request(metodo, caminho, corpo, cabecalhos)
        r = c.getresponse()
        saida = r.status, r.read().decode(), r.getheader("Location")
        c.close()
        return saida

    def coord(self, metodo, caminho, campos=None):
        return self.pedir(metodo, caminho, campos, Silencioso.senha)

    def criar(self, titulo="Abertura"):
        return self.coord("POST", "/coordenacao/atividade", {
            "titulo": titulo, "inicio": "2027-05-10T19:00", "fim": "2027-05-10T21:00", "vagas": 5})

    def test_caminho_completo(self):
        self.assertEqual(self.criar()[0], 303)
        st, _, minha = self.pedir("POST", "/inscrever", {"nome": "Ana", "email": "ana@x.org", "atividade": 1})
        self.assertEqual(st, 303)
        self.assertEqual(self.pedir("GET", minha)[0], 200)
        self.assertEqual(self.pedir("GET", minha.replace("minha", "certificado"))[0], 400)
        self.coord("POST", "/coordenacao/chamada", {"id": 1, "presente": 1})
        self.coord("POST", "/coordenacao/encerrar", {})
        st, html, _ = self.pedir("GET", minha.replace("minha", "certificado"))
        self.assertEqual(st, 200)
        self.assertIn("<b>2h</b>", html)
        codigo = html.split("validação: <b>")[1].split("<")[0]
        self.assertIn("Válido: Ana", self.pedir("GET", "/validar?codigo=" + codigo)[1])

    def test_coordenacao_exige_senha(self):
        for metodo, caminho in (("GET", "/coordenacao"), ("GET", "/coordenacao/chamada?id=1"),
                                ("POST", "/coordenacao/encerrar"), ("POST", "/coordenacao/atividade"),
                                ("POST", "/coordenacao/chamada")):
            self.assertEqual(self.pedir(metodo, caminho)[0], 401, caminho)
            self.assertEqual(self.pedir(metodo, caminho, senha="errada")[0], 401, caminho)
        self.assertEqual(self.pedir("GET", "/coordenacao", Authorization="Basic %%%")[0], 401)

    def test_outro_site_nao_envia_formulario(self):
        st, _, _ = self.pedir("POST", "/coordenacao/encerrar", {}, Silencioso.senha, Origin="http://mau.example")
        self.assertEqual(st, 403)

    def test_formulario_do_proprio_site(self):
        self.criar()
        host = "127.0.0.1:%d" % self.srv.server_address[1]
        st, _, _ = self.pedir("POST", "/inscrever", {"nome": "Ana", "email": "ana@x.org", "atividade": 1},
                              Origin="http://" + host)
        self.assertEqual(st, 303)
        c = http.client.HTTPConnection(*self.srv.server_address)
        c.request("GET", "/")
        # Com no-referrer o navegador mandaria Origin: null (ver registro, etapa 3a).
        self.assertEqual(c.getresponse().getheader("Referrer-Policy"), "same-origin")
        c.close()

    def test_html_escapado(self):
        self.criar("<script>1</script>")
        self.assertNotIn("<script>1", self.pedir("GET", "/")[1])
        self.assertNotIn("<script>1", paginas.certificado({"nome": "<script>1", "minutos": 60, "validacao": "X"}))
        self.assertNotIn('"><script>', self.pedir("GET", '/validar?codigo=%22%3E%3Cscript%3E')[1])

    def test_entradas_tortas(self):
        self.assertEqual(self.pedir("GET", "/nada")[0], 404)
        self.assertEqual(self.pedir("GET", "/minha?c=nada")[0], 400)
        self.assertEqual(self.pedir("POST", "/inscrever", {"nome": "A", "email": "a@x.org", "atividade": "x"})[0], 400)
        self.assertEqual(self.coord("GET", "/coordenacao/chamada?id=99")[0], 400)
        self.assertEqual(self.pedir("POST", "/inscrever", **{"Content-Length": "999999999"})[0], 413)

    def test_corrida_pela_ultima_vaga(self):
        self.coord("POST", "/coordenacao/atividade", {
            "titulo": "Uma vaga", "inicio": "2027-05-10T19:00", "fim": "2027-05-10T21:00", "vagas": 1})
        status = []
        fila = [threading.Thread(target=lambda n=n: status.append(self.pedir(
            "POST", "/inscrever", {"nome": "P", "email": f"p{n}@x.org", "atividade": 1})[0])) for n in range(8)]
        for t in fila:
            t.start()
        for t in fila:
            t.join()
        self.assertEqual(sorted(status), [303] + [400] * 7)
