"""
Testes automatizados do Gerenciador de Tabela de Símbolos.

Executar:
    python -m unittest test_symbol_table.py -v
"""

from __future__ import annotations

import unittest

from symbol_table import EntradaSimbolo, ErroTabelaSimbolos, GerenciadorTabelaSimbolos


class TestDeclararEBuscarGlobal(unittest.TestCase):
    def setUp(self) -> None:
        self.tabela = GerenciadorTabelaSimbolos()

    def test_declarar_e_buscar_no_global(self) -> None:
        self.tabela.declarar("idade", "int")
        entrada = self.tabela.buscar("idade")
        self.assertEqual(entrada, EntradaSimbolo("idade", "int", 0))

    def test_varias_variaveis_no_global(self) -> None:
        self.tabela.declarar("a", "int")
        self.tabela.declarar("b", "float")
        self.assertEqual(self.tabela.buscar("a").tipo, "int")
        self.assertEqual(self.tabela.buscar("b").tipo, "float")


class TestEscoposAninhados(unittest.TestCase):
    def setUp(self) -> None:
        self.tabela = GerenciadorTabelaSimbolos()

    def test_shadowing(self) -> None:
        self.tabela.declarar("x", "int")
        self.tabela.entrar_escopo()
        self.tabela.declarar("x", "string")
        self.assertEqual(self.tabela.buscar("x"), EntradaSimbolo("x", "string", 1))

    def test_heranca_do_escopo_externo(self) -> None:
        self.tabela.declarar("y", "float")
        self.tabela.entrar_escopo()
        self.assertEqual(self.tabela.buscar("y"), EntradaSimbolo("y", "float", 0))

    def test_mesmo_nome_em_escopos_diferentes_e_permitido(self) -> None:
        self.tabela.declarar("v", "int")
        self.tabela.entrar_escopo()
        self.tabela.declarar("v", "bool")
        self.assertEqual(self.tabela.buscar("v").tipo, "bool")
        self.tabela.sair_escopo()
        self.assertEqual(self.tabela.buscar("v").tipo, "int")

    def test_variavel_some_apos_sair_escopo(self) -> None:
        self.tabela.entrar_escopo()
        self.tabela.declarar("local", "int")
        self.tabela.sair_escopo()
        with self.assertRaises(ErroTabelaSimbolos):
            self.tabela.buscar("local")

    def test_tres_niveis_de_aninhamento(self) -> None:
        self.tabela.declarar("g", "int")
        self.tabela.entrar_escopo()
        self.tabela.declarar("n1", "float")
        self.tabela.entrar_escopo()
        self.tabela.declarar("n2", "bool")
        self.assertEqual(self.tabela.nivel_escopo_atual, 2)
        self.assertEqual(self.tabela.buscar("g").escopo_nivel, 0)
        self.assertEqual(self.tabela.buscar("n1").escopo_nivel, 1)
        self.assertEqual(self.tabela.buscar("n2").escopo_nivel, 2)


class TestErros(unittest.TestCase):
    def setUp(self) -> None:
        self.tabela = GerenciadorTabelaSimbolos()

    def test_redeclaracao_no_mesmo_escopo(self) -> None:
        self.tabela.declarar("k", "int")
        with self.assertRaises(ErroTabelaSimbolos) as ctx:
            self.tabela.declarar("k", "float")
        self.assertIn("Redeclaração", str(ctx.exception))

    def test_variavel_nao_declarada(self) -> None:
        with self.assertRaises(ErroTabelaSimbolos) as ctx:
            self.tabela.buscar("fantasma")
        self.assertIn("não declarada", str(ctx.exception))

    def test_nome_vazio_em_declarar(self) -> None:
        with self.assertRaises(ErroTabelaSimbolos):
            self.tabela.declarar("   ", "int")

    def test_nome_vazio_em_buscar(self) -> None:
        with self.assertRaises(ErroTabelaSimbolos):
            self.tabela.buscar("")

    def test_nao_pode_sair_do_escopo_global(self) -> None:
        with self.assertRaises(ErroTabelaSimbolos) as ctx:
            self.tabela.sair_escopo()
        self.assertIn("global", str(ctx.exception))


class TestUtilitarios(unittest.TestCase):
    def test_remove_espacos_em_nome_e_tipo(self) -> None:
        tabela = GerenciadorTabelaSimbolos()
        tabela.declarar("  nome  ", "  double  ")
        self.assertEqual(tabela.buscar("nome"), EntradaSimbolo("nome", "double", 0))

    def test_dump_pilha_e_copia_independente(self) -> None:
        tabela = GerenciadorTabelaSimbolos()
        tabela.declarar("a", "int")
        copia = tabela.dump_pilha()
        copia[0]["a"] = "alterado"
        self.assertEqual(tabela.buscar("a").tipo, "int")

    def test_pilha_inicia_com_um_escopo_global(self) -> None:
        tabela = GerenciadorTabelaSimbolos()
        self.assertEqual(len(tabela.dump_pilha()), 1)


if __name__ == "__main__":
    unittest.main()
