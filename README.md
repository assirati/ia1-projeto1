# Projeto 1 — Inteligência Artificial 1

Busca em espaço de estados e satisfação de restrições, aplicadas à operação
de um centro de distribuição.

Leia `ENUNCIADO.md` para as regras completas. Este arquivo é só para você
colocar o projeto para rodar em cinco minutos.

---

## Começar

Requer Python 3.10 ou superior. No Windows, troque `python3` por `python`
em todos os comandos deste arquivo.

Clonem o repositório e instalem as dependências:

```bash
git clone https://github.com/assirati/ia1-projeto1.git
cd ia1-projeto1
python3 -m pip install -r requirements.txt
```

O `requirements.txt` instala `pandas` e `matplotlib`, que vocês vão usar
para análise e gráficos. Os scripts do repositório rodam só com a
biblioteca padrão.

Se o pip recusar a instalação com o erro `externally-managed-environment`
(comum em Linux e no Python do Homebrew), criem um ambiente virtual e
instalem dentro dele:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python3 -m pip install -r requirements.txt
```

Depois, gerem a instância do grupo:

```bash
python3 minha_instancia.py <matricula> <producao|computacao>
```

Use a matrícula do integrante mais velho do grupo. O mesmo par de números
vai valer para todas as entregas.

Exemplo:

```bash
python3 minha_instancia.py 20231234 computacao
```

Isso imprime o mapa do armazém e a tabela de caminhões. Guarde os dois
seeds que aparecem no topo. As seções 3 e 4 do `ENUNCIADO.md` explicam
como ler essa saída, com um exemplo de cada módulo.

## Primeiros resultados

```bash
python3 exemplos/exemplo_modulo1.py <matricula> <curso>
python3 exemplos/exemplo_modulo2.py <matricula> <curso>
```

Cada um roda as estratégias de referência e grava um CSV em `dados/`.

**Isso não é a entrega.** É o esqueleto para vocês adaptarem. O trabalho
que vale nota começa quando vocês perguntam por que os números saíram
assim.

O segundo script demora mais, porque algumas células levam até 60 segundos
para serem interrompidas.

## Sua submissão ao torneio

Editem os dois arquivos em `submissao/`:

| Arquivo         | O que implementar                                 |
| --------------- | ------------------------------------------------- |
| `heuristica.py` | uma heurística para o A\* do módulo 1             |
| `ordenacao.py`  | uma ordenação de variáveis para o CSP do módulo 2 |

Os dois já vêm com um exemplo funcional dentro. Substituam.

Antes de enviar:

```bash
python3 verificar_submissao.py <matricula> <curso>
```

Esse script roda as mesmas checagens do torneio, na sua instância e em
mais duas do pool. Ele diz se a submissão é **válida**, não se ela é boa.

Marcações:

- `[ok]` passou
- `[!]` aviso. Não impede o envio, mas você precisa saber explicar
- `[ERRO]` submissão inválida. Corrija antes de 21/09

### Entrega no Canvas

Quando o verificador disser "Submissão válida", gerem um zip com os dois
arquivos. Usem no nome a mesma matrícula da instância:

```bash
python3 -m zipfile -c submissao_<matricula>.zip submissao/heuristica.py submissao/ordenacao.py
```

O comando usa o próprio Python, então funciona igual em Windows, macOS e
Linux. Confiram o conteúdo antes de enviar:

```bash
python3 -m zipfile -l submissao_<matricula>.zip
```

A lista deve ter exatamente `heuristica.py` e `ordenacao.py`, sem pasta em
volta e sem outros arquivos. O torneio carrega cada arquivo sozinho, então
eles não podem importar outros arquivos de vocês.

Enviem o zip na tarefa do torneio no Canvas. Prazo: **21/09, 23h59**. Sem
segunda chamada.

## Formulários

Os dois formulários do projeto estão no repositório em Word. Preencham o
arquivo `.docx` (no Word, no LibreOffice ou no Google Docs) e enviem o
próprio `.docx` na tarefa correspondente do Canvas:

| Formulário | Quando | Onde enviar |
|---|---|---|
| `PRE_REGISTRO.docx` | até **16/09, 23h59**, antes de rodar qualquer experimento | tarefa do pré-registro no Canvas |
| `FICHA_REPLICACAO.docx` | na sessão de **28/09**, sobre o pacote do grupo auditado | tarefa da ficha no Canvas, ainda durante a sessão |

Os `.md` de mesmo nome têm o mesmo conteúdo, para ler aqui no GitHub.

---

## O que tem em cada lugar

```
ENUNCIADO.md              regras, prazos, pontuação
RUBRICA.md                critérios de correção de cada componente
BANCO_PERGUNTAS.md        as 24 perguntas da arguição, públicas
PRE_REGISTRO.docx         formulário a preencher e enviar no Canvas até 16/09
FICHA_REPLICACAO.docx     formulário a preencher e enviar no Canvas em 28/09
PRE_REGISTRO.md e         os mesmos formulários, para leitura
FICHA_REPLICACAO.md
histograma_calibracao.png distribuição de dificuldade dos seeds

minha_instancia.py        gera a sua instância
verificar_submissao.py    autoteste antes de enviar

submissao/                os dois arquivos que vocês entregam
exemplos/                 scripts de partida, geram CSV
dados/                    saída dos scripts (vazio no início)

engine/
  config.py               perfis de curso e atribuição de seeds
  gen_search.py           gerador de instâncias do módulo 1
  gen_csp.py              gerador de instâncias do módulo 2
  solve_search.py         A*, heurísticas de referência, busca gulosa
  solve_csp.py            backtracking, MRV, LCV, forward checking, AC-3
```

## Referência rápida da API

**Módulo 1**

```python
from engine import gen_search
from engine.solve_search import astar

inst = gen_search.generate(seed)
inst.depot                     # (linha, coluna) da doca
inst.items[i]                  # posição do item i, na ordem dos bits da máscara
inst.grid[l][c]                # 0 = livre, 1 = prateleira
inst.dist[alvo][celula]        # distância real; alvos: cada item e a doca

r = astar(inst, "real")        # "h0", "manhattan", "real", "mst"
r = astar(inst, "real", greedy=True)
r = astar(inst, minha_fabrica) # sua heurística

r["cost"] r["expanded"] r["generated"] r["ms"]
```

**Módulo 2**

```python
from engine import gen_csp
from engine.config import PERFIL
from engine.solve_csp import solve, verify

inst = gen_csp.generate(seed, **PERFIL["computacao"])
sol, st = solve(inst,
                var_order="mrv",       # "static", "mrv", "mrv_deg", ou função
                val_order="static",    # "static", "lcv"
                inference="fc",        # "none", "fc", "mac"
                time_limit_s=60)

st.backtracks st.assignments st.checks st.prunings st.ms st.solved
verify(inst, sol)
```

## Perguntas frequentes

**A instância de outro grupo é mais fácil que a minha?** \
Os seeds foram filtrados para uma banda estreita de dificuldade. A
distribuição está em `histograma_calibracao.png`. Diferença de até 5 vezes
em nós expandidos é esperada e não muda nenhuma conclusão qualitativa.

**Posso usar numpy, pandas, matplotlib?** \
Para análise e gráficos, sim. Nos dois arquivos de `submissao/`, não.
Apenas biblioteca padrão.

**Posso modificar o `engine/`?** \
Para experimentar, à vontade. Mas o torneio e a replicação ao vivo rodam
com a versão original, então não dependa das suas mudanças.

**Posso usar IA generativa?** \
Sim, sem restrição. Leia a seção 9 do enunciado: o pacote precisa
documentar um erro que a IA cometeu e como vocês detectaram.

**Meu script demora demais.** \
Reduza `time_limit_s` enquanto desenvolve e volte para 60 na medição
final. Só não omita as células censuradas do CSV.
