# Gerenciador de Tabela de Símbolos

Projeto da disciplina ** de Compiladores** (PBL): módulo que gerencia escopos aninhados usando uma **pilha de hash tables** (tabelas de símbolos em Python: `dict`), com os métodos `declarar(variavel, tipo)` e `buscar(variavel)`.

## Requisitos

- Python **3.10** ou superior
- Nenhuma dependência externa (stdlib apenas)

Verifique a versão:

```bash
python --version
```

No Windows, se `python` não funcionar, use `py`:

```bash
py --version
```

## Estrutura do projeto

```
.
├── README.md           # este arquivo
├── symbol_table.py     # GerenciadorTabelaSimbolos (pilha + hash tables)
├── main.py             # demonstração e modo interativo
├── test_symbol_table.py # testes automatizados (unittest)
├── relatorio.md        # rascunho do relatório (exportar para PDF)
└── .gitignore
```

## Como executar

Resumo dos comandos (na pasta raiz do repositório):

```bash
python main.py
python main.py --interativo
python -m unittest test_symbol_table.py -v
```

### Demonstração automática (recomendado para avaliação)

Na pasta raiz do repositório:

```bash
python main.py
```

Equivalente explícito:

```bash
python main.py --demo
```

No Windows (launcher):

```bash
py main.py
```

A saída mostra cada operação (`declarar`, `buscar`, `entrar_escopo`, `sair_escopo`), o resultado ou mensagem de erro, e o estado da **pilha de escopos** após cada passo.

### Modo interativo (teste manual)

Na pasta raiz do repositório:

```bash
python main.py --interativo
```

No Windows (launcher):

```bash
py main.py --interativo
```

O programa exibe o prompt `>`. Digite um comando por linha e pressione Enter.

Comandos no prompt:

| Comando | Exemplo | Descrição |
|---------|---------|-----------|
| `declarar` | `declarar contador int` ou `declarar contador = int` | Declara no escopo atual (sem `=` no início da linha) |
| `buscar` | `buscar contador` | Busca do escopo interno para o externo |
| `entrar` | `entrar` | Empilha novo escopo |
| `sair` | `sair` | Desempilha escopo (não remove o global) |
| `estado` | `estado` | Imprime a pilha de hash tables |
| `sair_programa` | `sair_programa` | Encerra o programa |

**Roteiro rápido de teste manual** (copie no prompt após `python main.py --interativo`):

```text
declarar x int
declarar y float
estado
buscar x
entrar
declarar x string
buscar x
buscar y
sair
buscar x
buscar fantasma
sair_programa
```

Saída esperada em resumo: `x` como `string` no escopo interno, `y` herdado do global, após `sair` o `x` volta a `int`, `buscar fantasma` gera erro de variável não declarada.

### Testes automatizados

Na pasta raiz do repositório:

```bash
python -m unittest test_symbol_table.py -v
```

Saída esperada: linhas com `ok` e resumo `OK` no final (15 testes).

No Windows:

```bash
py -m unittest test_symbol_table.py -v
```

## API principal (`symbol_table.py`)

```python
from symbol_table import GerenciadorTabelaSimbolos

tabela = GerenciadorTabelaSimbolos()  # já inicia com escopo global
tabela.declarar("a", "int")
tabela.entrar_escopo()
tabela.declarar("b", "float")
entrada = tabela.buscar("a")  # encontra no escopo global
tabela.sair_escopo()
```

- **`declarar(variavel, tipo)`** — insere no escopo do topo; erro se já existir nesse escopo.
- **`buscar(variavel)`** — percorre a pilha do topo para a base; erro se não existir.
- **`entrar_escopo()`** / **`sair_escopo()`** — gerenciam escopos aninhados.

## Autores

Nathan Rodrigues da Costa Silva, Nathan Rodrigues da Costa Silva e Thalita Pereira de Andrade.
