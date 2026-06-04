"""
Demonstração do Gerenciador de Tabela de Símbolos.
Execute: python main.py
Modos: python main.py --demo | python main.py --interativo
Testes: python -m unittest test_symbol_table.py -v
"""

from __future__ import annotations

import argparse
import sys

from symbol_table import ErroTabelaSimbolos, GerenciadorTabelaSimbolos


def _imprimir_estado(gerenciador: GerenciadorTabelaSimbolos, titulo: str) -> None:
    print(f"\n--- {titulo} ---")
    print(gerenciador.formatar_estado())


def _executar_passo(
    gerenciador: GerenciadorTabelaSimbolos,
    descricao: str,
    acao,
) -> None:
    print(f"\n>> {descricao}")
    try:
        resultado = acao()
        if resultado is not None:
            print(f"   Resultado: {resultado}")
    except ErroTabelaSimbolos as erro:
        print(f"   ERRO: {erro}")
    _imprimir_estado(gerenciador, "Pilha de escopos (hash tables)")


def rodar_demo() -> None:
    print("=" * 60)
    print("Gerenciador de Tabela de Símbolos — Casos de demonstração")
    print("=" * 60)

    g = GerenciadorTabelaSimbolos()

    _executar_passo(
        g,
        "declarar(x, int) no escopo global",
        lambda: g.declarar("x", "int"),
    )
    _executar_passo(
        g,
        "declarar(y, float) no escopo global",
        lambda: g.declarar("y", "float"),
    )
    _executar_passo(
        g,
        "buscar(x) — deve encontrar no global",
        lambda: g.buscar("x"),
    )

    _executar_passo(g, "entrar_escopo() — função/bloco interno", g.entrar_escopo)
    _executar_passo(
        g,
        "declarar(x, string) no escopo interno (shadowing)",
        lambda: g.declarar("x", "string"),
    )
    _executar_passo(
        g,
        "buscar(x) — deve retornar tipo do escopo interno",
        lambda: g.buscar("x"),
    )
    _executar_passo(
        g,
        "buscar(y) — herdado do escopo global",
        lambda: g.buscar("y"),
    )

    _executar_passo(g, "entrar_escopo() — segundo nível aninhado", g.entrar_escopo)
    _executar_passo(
        g,
        "declarar(z, bool) no escopo mais interno",
        lambda: g.declarar("z", "bool"),
    )
    _executar_passo(
        g,
        "buscar(z)",
        lambda: g.buscar("z"),
    )

    _executar_passo(
        g,
        "declarar(temp, int) no escopo mais interno",
        lambda: g.declarar("temp", "int"),
    )
    _executar_passo(
        g,
        "declarar(temp, float) no mesmo escopo — redeclaração (erro esperado)",
        lambda: g.declarar("temp", "float"),
    )
    _executar_passo(
        g,
        "buscar(inexistente) — variável não declarada",
        lambda: g.buscar("inexistente"),
    )

    _executar_passo(g, "sair_escopo() — volta ao escopo intermediário", g.sair_escopo)
    _executar_passo(
        g,
        "buscar(x) após sair — tipo string do escopo intermediário",
        lambda: g.buscar("x"),
    )

    _executar_passo(g, "sair_escopo() — volta ao global", g.sair_escopo)
    _executar_passo(
        g,
        "buscar(x) no global — tipo int original",
        lambda: g.buscar("x"),
    )

    print("\n" + "-" * 60)
    print("Casos extras")
    print("-" * 60)

    g2 = GerenciadorTabelaSimbolos()
    _executar_passo(
        g2,
        "declarar(  nome  ,  double  ) — remove espaços",
        lambda: g2.declarar("  nome  ", "  double  "),
    )
    _executar_passo(
        g2,
        "buscar(nome) após normalização",
        lambda: g2.buscar("nome"),
    )

    g3 = GerenciadorTabelaSimbolos()
    _executar_passo(
        g3,
        "declarar(local, int) em escopo interno e sair — some da busca",
        lambda: (g3.entrar_escopo(), g3.declarar("local", "int"), g3.sair_escopo()),
    )
    _executar_passo(
        g3,
        "buscar(local) após desempilhar escopo",
        lambda: g3.buscar("local"),
    )

    g4 = GerenciadorTabelaSimbolos()
    _executar_passo(
        g4,
        "sair_escopo() só com global — erro esperado",
        g4.sair_escopo,
    )

    print("\n" + "=" * 60)
    print("Demonstração concluída.")
    print("=" * 60)


def _tokenizar_comando(linha: str) -> list[str]:
    """Remove '=' solto no início ou entre nome e tipo (ex.: declarar x = int)."""
    partes = linha.split()
    while partes and partes[0] == "=":
        partes.pop(0)
    return partes


def _parse_declarar_args(partes: list[str]) -> tuple[str, str] | None:
    """partes: ['declarar', nome, ...tipo...]"""
    if len(partes) < 3 or partes[0].lower() != "declarar":
        return None
    nome = partes[1]
    resto = [p for p in partes[2:] if p != "="]
    if not resto:
        return None
    return nome, " ".join(resto)


def rodar_interativo() -> None:
    g = GerenciadorTabelaSimbolos()
    ajuda = (
        "Comandos: declarar <nome> <tipo> | declarar <nome> = <tipo> | buscar <nome> | "
        "entrar | sair | estado | ajuda | sair_programa"
    )
    print("Modo interativo — Gerenciador de Tabela de Símbolos")
    print(ajuda)
    _imprimir_estado(g, "Estado inicial")

    while True:
        try:
            linha = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if not linha:
            continue

        partes = _tokenizar_comando(linha)
        if not partes:
            continue

        cmd = partes[0].lower()

        try:
            if cmd in ("sair_programa", "quit", "exit"):
                break
            if cmd == "ajuda":
                print(ajuda)
            elif cmd == "estado":
                _imprimir_estado(g, "Pilha atual")
            elif cmd == "entrar":
                g.entrar_escopo()
                print("Novo escopo empilhado.")
                _imprimir_estado(g, "Pilha atual")
            elif cmd == "sair":
                g.sair_escopo()
                print("Escopo desempilhado.")
                _imprimir_estado(g, "Pilha atual")
            elif cmd == "declarar":
                args = _parse_declarar_args(partes)
                if args is None:
                    print(
                        "Uso: declarar <nome> <tipo>  ou  declarar <nome> = <tipo>"
                    )
                    continue
                nome, tipo = args
                entrada = g.declarar(nome, tipo)
                print(f"Declarado: {entrada}")
                _imprimir_estado(g, "Pilha atual")
            elif cmd == "buscar" and len(partes) >= 2:
                entrada = g.buscar(partes[1])
                print(f"Encontrado: {entrada}")
            else:
                print(f"Comando inválido. {ajuda}")
        except ErroTabelaSimbolos as erro:
            print(f"ERRO: {erro}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gerenciador de Tabela de Símbolos (escopos aninhados)."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Executa a demonstração automática (padrão).",
    )
    parser.add_argument(
        "--interativo",
        action="store_true",
        help="Modo interativo no terminal.",
    )
    args = parser.parse_args()

    if args.interativo:
        rodar_interativo()
    else:
        rodar_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
