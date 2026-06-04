"""
Gerenciador de Tabela de Símbolos com escopos aninhados.

Estruturas: pilha (list) de tabelas de símbolos (dict / hash table).
API: declarar(variavel, tipo), buscar(variavel), entrar_escopo(), sair_escopo().
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ErroTabelaSimbolos(Exception):
    """Erro semântico na tabela de símbolos."""


@dataclass(frozen=True)
class EntradaSimbolo:
    nome: str
    tipo: str
    escopo_nivel: int


class GerenciadorTabelaSimbolos:
    """
    Pilha de hash tables: cada nível da pilha é um escopo.
    O topo da pilha é o escopo atual (mais interno).
    """

    def __init__(self) -> None:
        self._pilha_escopos: list[dict[str, str]] = []
        self.entrar_escopo()

    @property
    def nivel_escopo_atual(self) -> int:
        return len(self._pilha_escopos) - 1

    def entrar_escopo(self) -> None:
        """Empilha uma nova hash table (escopo vazio)."""
        self._pilha_escopos.append({})

    def sair_escopo(self) -> None:
        """Remove o escopo do topo; não permite remover o escopo global."""
        if len(self._pilha_escopos) <= 1:
            raise ErroTabelaSimbolos(
                "Não é possível sair do escopo global (pilha com um único nível)."
            )
        self._pilha_escopos.pop()

    def declarar(self, variavel: str, tipo: str) -> EntradaSimbolo:
        """
        Declara `variavel` com `tipo` apenas no escopo atual (topo da pilha).
        Redeclaração no mesmo escopo gera erro.
        """
        nome = variavel.strip()
        if not nome:
            raise ErroTabelaSimbolos("Nome de variável inválido (vazio).")

        escopo_atual = self._pilha_escopos[-1]
        if nome in escopo_atual:
            raise ErroTabelaSimbolos(
                f"Redeclaração de '{nome}' no escopo nível {self.nivel_escopo_atual}."
            )

        escopo_atual[nome] = tipo.strip()
        return EntradaSimbolo(nome=nome, tipo=tipo.strip(), escopo_nivel=self.nivel_escopo_atual)

    def buscar(self, variavel: str) -> EntradaSimbolo:
        """
        Busca `variavel` do escopo mais interno para o mais externo.
        Retorna a primeira ocorrência encontrada (shadowing do escopo interno).
        """
        nome = variavel.strip()
        if not nome:
            raise ErroTabelaSimbolos("Nome de variável inválido (vazio).")

        for nivel, tabela in enumerate(reversed(self._pilha_escopos)):
            escopo_nivel = len(self._pilha_escopos) - 1 - nivel
            if nome in tabela:
                return EntradaSimbolo(
                    nome=nome,
                    tipo=tabela[nome],
                    escopo_nivel=escopo_nivel,
                )

        raise ErroTabelaSimbolos(
            f"Variável '{nome}' não declarada em nenhum escopo acessível."
        )

    def dump_pilha(self) -> list[dict[str, str]]:
        """Cópia superficial da pilha (para depuração e demonstração)."""
        return [dict(escopo) for escopo in self._pilha_escopos]

    def formatar_estado(self) -> str:
        linhas: list[str] = []
        for i, escopo in enumerate(self._pilha_escopos):
            rotulo = "global" if i == 0 else f"escopo_{i}"
            conteudo = ", ".join(f"{k}:{v}" for k, v in sorted(escopo.items())) or "(vazio)"
            marcador = " <- atual" if i == len(self._pilha_escopos) - 1 else ""
            linhas.append(f"  [{rotulo}]{marcador} {{ {conteudo} }}")
        return "\n".join(linhas)
