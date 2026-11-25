"""Esquema e conexão SQLite."""
import sqlite3
from pathlib import Path

ARQUIVO = Path(__file__).with_name("semana.db")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS atividade (
    id      INTEGER PRIMARY KEY,
    titulo  TEXT NOT NULL,
    inicio  TEXT NOT NULL,          -- AAAA-MM-DDTHH:MM
    fim     TEXT NOT NULL,
    vagas   INTEGER NOT NULL CHECK (vagas > 0)
);
CREATE TABLE IF NOT EXISTS pessoa (
    id          INTEGER PRIMARY KEY,
    nome        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    codigo      TEXT NOT NULL UNIQUE,   -- link pessoal
    certificado TEXT UNIQUE             -- código de validação, criado na emissão
);
CREATE TABLE IF NOT EXISTS inscricao (
    pessoa_id    INTEGER NOT NULL REFERENCES pessoa(id),
    atividade_id INTEGER NOT NULL REFERENCES atividade(id),
    presente     INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (pessoa_id, atividade_id)
);
CREATE TABLE IF NOT EXISTS evento (
    id        INTEGER PRIMARY KEY CHECK (id = 1),
    encerrado INTEGER NOT NULL DEFAULT 0
);
INSERT OR IGNORE INTO evento (id) VALUES (1);
"""


def conectar(arquivo=ARQUIVO):
    con = sqlite3.connect(arquivo, isolation_level=None)  # transações explícitas
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript(ESQUEMA)
    return con
