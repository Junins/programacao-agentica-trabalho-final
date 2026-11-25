"""Executa as situações das perguntas e mostra o que o sistema faz de verdade.

Uso: python experimento/conferir.py a|b     (depois do commit das suas respostas)
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "produto"))
import banco
import servico as s


def tenta(f, *args):
    try:
        return f(*args)
    except s.ErroRegra as erro:
        return f"RECUSADO: {erro}"


def novo(*horarios, vagas=9):
    con = banco.conectar(":memory:")
    return con, [s.criar_atividade(con, f"At{n}", i, f, vagas) for n, (i, f) in enumerate(horarios, 1)]


def hora(h, duracao=1):
    return f"2027-05-10T{h:02}:00", f"2027-05-10T{h + duracao:02}:00"


def pid(con, codigo):
    return s.pessoa_por_codigo(con, codigo)["id"]


def http(roteiro):
    import unittest
    from testes import test_http

    class Sonda(test_http.Http):
        def runTest(self):
            roteiro(self)
    resultado = unittest.TestResult()
    Sonda().run(resultado)
    for _, traco in resultado.errors + resultado.failures:
        print(traco)


def a1():
    def r(t):
        t.criar()
        st, _, destino = t.pedir("POST", "/inscrever", {"nome": "Ana", "email": "a@x.org", "atividade": 1})
        print(f"  status {st}, vai para {destino.split('=')[0]}=<código pessoal>")
        print(f"  mesmo endereço sem o código: status {t.pedir('GET', '/minha')[0]}")
    http(r)


def a2():
    con, [x] = novo(hora(8))
    ids = [pid(con, s.inscrever(con, n, f"{n}@x.org", [x])) for n in ("Ana", "Beto")]
    s.gravar_chamada(con, x, ids)
    s.gravar_chamada(con, x, ids[1:])
    print(" ", {p["nome"]: bool(p["presente"]) for p in s.lista_de_chamada(con, x)})


def a3():
    con, [x] = novo(hora(8))
    c = s.inscrever(con, "Ana", "a@x.org", [x])
    s.gravar_chamada(con, x, [pid(con, c)])
    print(" ", tenta(s.emitir_certificado, con, c))


def a4():
    con, xs = novo(*(hora(h) for h in (8, 9, 10, 11)))
    ana, beto = s.inscrever(con, "Ana", "a@x.org", xs), s.inscrever(con, "Beto", "b@x.org", xs[:1])
    s.gravar_chamada(con, xs[0], [pid(con, ana), pid(con, beto)])
    s.gravar_chamada(con, xs[1], [pid(con, ana)])
    s.encerrar(con)
    print("  Ana:", tenta(s.emitir_certificado, con, ana))
    print("  Beto:", tenta(s.emitir_certificado, con, beto))


def a5():
    con, xs = novo(hora(8), hora(9))
    s.inscrever(con, "Ana", "a@x.org", xs[:1])
    print(" ", tenta(s.inscrever, con, "Ana", "a@x.org", xs[1:]))


def a6():
    con, xs = novo(hora(8), hora(9), vagas=1)
    s.inscrever(con, "Ana", "a@x.org", xs[:1])
    print(" ", tenta(s.inscrever, con, "Beto", "b@x.org", xs))
    print("  inscritos com o e-mail de Beto:",
          con.execute("SELECT COUNT(*) FROM pessoa WHERE email = ?", ("b@x.org",)).fetchone()[0])


def b1():
    def r(t):
        print("  sem senha: status", t.pedir("GET", "/coordenacao")[0])
        print("  usuário inventado, senha certa: status", t.coord("GET", "/coordenacao")[0])
    http(r)


def certificada(duracoes, presentes):
    con, xs = novo(*(hora(8 + sum(duracoes[:n]), d) for n, d in enumerate(duracoes)))
    c = s.inscrever(con, "Ana", "a@x.org", xs)
    for n in presentes:
        s.gravar_chamada(con, xs[n], [pid(con, c)])
    s.encerrar(con)
    return con, c


def b2():
    con, c = certificada([1], [0])
    print(" ", s.validar(con, s.emitir_certificado(con, c)["validacao"].lower()))


def b3():
    con, c = certificada([1], [0])
    um, dois = (s.emitir_certificado(con, c)["validacao"] for _ in range(2))
    print("  mesmo código" if um == dois else "  código mudou")


def b4():
    con, c = certificada([4, 1], [0])
    print(" ", tenta(s.emitir_certificado, con, c))


def b5():
    con, xs = novo(("2027-05-10T23:00", "2027-05-11T01:00"), ("2027-05-11T00:30", "2027-05-11T02:00"))
    print(" ", tenta(s.inscrever, con, "Ana", "a@x.org", xs))


def b6():
    con, [x, y] = novo(hora(8), hora(9))
    joao = pid(con, s.inscrever(con, "João", "j@x.org", [y]))
    print("  na lista de chamada:", [p["nome"] for p in s.lista_de_chamada(con, x)])
    print("  forçando:", tenta(s.gravar_chamada, con, x, [joao]))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("a", "b"):
        sys.exit(__doc__)
    for n in range(1, 7):
        print(f"{n}.")
        try:
            globals()[f"{sys.argv[1]}{n}"]()
        except Exception as erro:  # o código pode ter mudado nas manutenções
            print(f"  não consegui executar: {erro!r}")
