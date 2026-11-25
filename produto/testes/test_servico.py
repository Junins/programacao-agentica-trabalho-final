import unittest

import banco
import servico as s


class Caso(unittest.TestCase):
    def setUp(self):
        self.con = banco.conectar(":memory:")
        self.a = s.criar_atividade(self.con, "Abertura", "2027-05-10T19:00", "2027-05-10T20:00", 2)
        self.b = s.criar_atividade(self.con, "Oficina", "2027-05-10T20:00", "2027-05-10T23:00", 2)
        self.c = s.criar_atividade(self.con, "Debate", "2027-05-10T19:30", "2027-05-10T20:30", 2)

    def tearDown(self):
        self.con.close()

    def recusa(self, trecho, f, *args):
        with self.assertRaises(s.ErroRegra) as erro:
            f(self.con, *args)
        self.assertIn(trecho, str(erro.exception))

    def id_de(self, codigo):
        return s.pessoa_por_codigo(self.con, codigo)["id"]

    def test_caminho_completo(self):
        codigo = s.inscrever(self.con, "Ana", "ana@x.org", [self.a, self.b])
        s.gravar_chamada(self.con, self.b, [self.id_de(codigo)])
        s.encerrar(self.con)
        cert = s.emitir_certificado(self.con, codigo)      # 3 de 4 horas = 75%
        self.assertEqual(cert["minutos"], 180)
        self.assertEqual(s.emitir_certificado(self.con, codigo), cert)
        self.assertEqual(s.validar(self.con, cert["validacao"].lower())["nome"], "Ana")
        self.assertIsNone(s.validar(self.con, "NADA"))

    def test_abaixo_do_minimo(self):
        codigo = s.inscrever(self.con, "Ana", "ana@x.org", [self.a, self.b])
        s.gravar_chamada(self.con, self.a, [self.id_de(codigo)])
        s.encerrar(self.con)
        self.recusa("75%", s.emitir_certificado, codigo)

    def test_certificado_so_depois_de_encerrar(self):
        codigo = s.inscrever(self.con, "Ana", "ana@x.org", [self.a])
        self.recusa("encerramento", s.emitir_certificado, codigo)

    def test_conflito_nao_deixa_rastro(self):
        self.recusa("conflito", s.inscrever, "Ana", "ana@x.org", [self.a, self.c])
        self.assertEqual(self.con.execute("SELECT COUNT(*) FROM pessoa").fetchone()[0], 0)

    def test_horarios_encostados_nao_conflitam(self):
        s.inscrever(self.con, "Ana", "ana@x.org", [self.a, self.b])

    def test_vagas(self):
        for n in range(2):
            s.inscrever(self.con, "P", f"p{n}@x.org", [self.a])
        self.recusa("vaga", s.inscrever, "P", "p3@x.org", [self.a])

    def test_email_repetido(self):
        s.inscrever(self.con, "Ana", "ana@x.org", [self.a])
        self.recusa("já tem", s.inscrever, "Ana", " ANA@x.org ", [self.b])

    def test_chamada_substitui_e_recusa_estranho(self):
        codigo = s.inscrever(self.con, "Ana", "ana@x.org", [self.a])
        p = self.id_de(codigo)
        s.gravar_chamada(self.con, self.a, [p])
        s.gravar_chamada(self.con, self.a, [])
        self.assertEqual(s.lista_de_chamada(self.con, self.a)[0]["presente"], 0)
        self.recusa("não se inscreveu", s.gravar_chamada, self.b, [p])

    def test_encerrado_trava_mudancas(self):
        s.encerrar(self.con)
        self.recusa("encerrado", s.inscrever, "Ana", "ana@x.org", [self.a])
        self.recusa("encerrado", s.gravar_chamada, self.a, [])
        self.recusa("encerrado", s.encerrar)

    def test_atividade_invalida(self):
        self.recusa("depois", s.criar_atividade, "X", "2027-05-10T20:00", "2027-05-10T20:00", 1)
        self.recusa("inválido", s.criar_atividade, "X", "ontem", "hoje", 1)
        self.recusa("uma vaga", s.criar_atividade, "X", "2027-05-10T20:00", "2027-05-10T21:00", 0)
        self.recusa("inexistente", s.inscrever, "Ana", "a@x.org", [999])

    def test_atividade_repetida_no_formulario_conta_uma_vez(self):
        codigo = s.inscrever(self.con, "Ana", "ana@x.org", [self.a, self.a])
        self.assertEqual(len(s.inscricoes_da_pessoa(self.con, self.id_de(codigo))), 1)

    def test_encerrado_nao_aceita_atividade_nova(self):
        s.encerrar(self.con)
        self.recusa("encerrado", s.criar_atividade, "X", "2027-05-10T20:00", "2027-05-10T21:00", 1)
