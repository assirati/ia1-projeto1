# Projeto 1 — Inteligência Artificial 1

Busca em espaço de estados e satisfação de restrições, aplicadas à operação
de um centro de distribuição.

Leia `ENUNCIADO.md` para as regras completas. Este arquivo é só para você
colocar o projeto para rodar em cinco minutos.

---

## Começar

Requer Python 3.10 ou superior. Nada precisa ser instalado para rodar o
básico.

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
seeds que aparecem no topo.

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

| Arquivo | O que implementar |
|---|---|
| `heuristica.py` | uma heurística para o A* do módulo 1 |
| `ordenacao.py` | uma ordenação de variáveis para o CSP do módulo 2 |

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

Prazo: **21/09, 23h59**. Sem segunda chamada.

---

## O que tem em cada lugar

```
ENUNCIADO.md              regras, prazos, pontuação
RUBRICA.md                critérios de correção de cada componente
BANCO_PERGUNTAS.md        as 24 perguntas da arguição, públicas
PRE_REGISTRO.md           formulário a entregar em 16/09
FICHA_REPLICACAO.md       o que será preenchido em 28/09
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

**A instância de outro grupo é mais fácil que a minha?**
Os seeds foram filtrados para uma banda estreita de dificuldade. A
distribuição está em `histograma_calibracao.png`. Diferença de até 5 vezes
em nós expandidos é esperada e não muda nenhuma conclusão qualitativa.

**Posso usar numpy, pandas, matplotlib?**
Para análise e gráficos, sim. Nos dois arquivos de `submissao/`, não.
Apenas biblioteca padrão.

**Posso modificar o `engine/`?**
Para experimentar, à vontade. Mas o torneio e a replicação ao vivo rodam
com a versão original, então não dependa das suas mudanças.

**Posso usar IA generativa?**
Sim, sem restrição. Leia a seção 9 do enunciado: o pacote precisa
documentar um erro que a IA cometeu e como vocês detectaram.

**Meu script demora demais.**
Reduza `time_limit_s` enquanto desenvolve e volte para 60 na medição
final. Só não omita as células censuradas do CSV.
