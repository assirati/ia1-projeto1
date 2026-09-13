# Pré-registro de Hipóteses

**Entrega: 16/09/2026, 23h59. Sem prorrogação.**

Preencham o `PRE_REGISTRO.docx` e enviem o arquivo na tarefa do
pré-registro no Canvas.

Grupo: ______________________  Curso: ( ) Produção ( ) Computação
Integrantes: ______________________________________________
Seed de busca: __________  Seed de CSP: __________

---

## Como isto é avaliado

Vale 1,5 ponto. A nota **não depende de acertar**.

Ela depende de duas coisas:

1. A predição é falsificável? Tem número, tem faixa, dá para dizer se
   errou.
2. Depois, no pôster, vocês explicam a divergência de forma testável?

Predição vaga e certa vale pouco. Predição arriscada e errada, bem
analisada depois, vale muito.

**Não rodem nada antes de preencher.** Vocês já têm o enunciado, os
histogramas de calibração e o material de aula. É com isso que se prevê.

Justificativa: no máximo cinco linhas por item.

---

## Bloco A — Busca (obrigatório)

### A1. Custo uniforme contra A*

Quantos nós o A* com distância real expande, em proporção ao custo
uniforme, na **sua** instância?

> Predição: A* expandirá entre ______ % e ______ % dos nós do custo
> uniforme.

Justificativa:

```


```

### A2. Busca gulosa

A busca gulosa expande muito menos nós. Qual o preço disso?

> Predição: a rota da busca gulosa será entre ______ % e ______ % mais
> longa que a rota ótima.

Justificativa:

```


```

### A3. Heurística própria

Descrevam em uma frase a heurística que pretendem implementar.

```

```

> Predição: ela expandirá entre ______ % e ______ % dos nós do A* com
> distância real.

> Ela é admissível? ( ) Sim ( ) Não ( ) Não sabemos ainda

Justificativa:

```


```

---

## Bloco B — CSP (obrigatório)

### B1. Ordenação contra inferência

Esta é a pergunta central do módulo. Considerem quatro configurações:

| # | Ordenação | Inferência |
|---|---|---|
| I | estática | nenhuma |
| II | estática | forward checking |
| III | MRV | nenhuma |
| IV | MRV | forward checking |

> Ordenem as quatro da que fará **mais** backtracks para a que fará
> **menos**:
>
> 1º ______  2º ______  3º ______  4º ______

Agora a parte que interessa:

> Entre II (só inferência) e III (só ordenação), qual fará menos
> backtracks? ______
>
> Por qual fator? ______ vezes

Justificativa:

```


```

### B2. AC-3

> Predição: MAC (AC-3) fará entre ______ e ______ backtracks na nossa
> instância.

> Predição: o tempo de MAC será ______ vezes o tempo de MRV com forward
> checking. (Pode ser menor que 1.)

Justificativa:

```


```

### B3. Censura

> Predição: das 6 células, ______ delas não terminarão em 60 segundos.

Justificativa:

```


```

---

## Bloco C — Torneio de heurísticas (obrigatório)

Vocês vão submeter uma heurística de busca e uma ordenação de variáveis
para rodar contra as instâncias de **todos** os colegas.

### C1. Generalização

> Predição: nossa heurística ficará entre a ______ª e a ______ª posição
> entre as heurísticas submetidas pela turma, em nós expandidos na média.

> Predição: a diferença entre o desempenho dela na **nossa** instância e a
> média sobre as 30 instâncias do pool será de cerca de ______ %.

Justificativa:

```


```

### C2. Admissibilidade e consistência

> Nossa heurística é admissível? ( ) Sim ( ) Não ( ) Não sabemos
>
> Nossa heurística é consistente? ( ) Sim ( ) Não ( ) Não sabemos
>
> Se as duas respostas forem diferentes, expliquem por quê:

```


```

> Predição: quantas das 30 instâncias produzirão contraexemplo de
> admissibilidade? ______

### C3. Inadmissibilidade na tabela

Alguns grupos vão submeter heurísticas inadmissíveis, de propósito ou não.

> Predição: a heurística mais rápida do ranking (menos nós) será
> admissível? ( ) Sim ( ) Não
>
> Predição: a heurística inadmissível mais rápida expandirá cerca de
> ______ % dos nós da melhor admissível, e devolverá rota cerca de
> ______ % mais longa.

Justificativa:

```


```

---

## Bloco D — Uma predição de vocês (obrigatório)

Formulem **uma** pergunta que o enunciado não fez, sobre qualquer um dos
três módulos, e prevejam a resposta com número.

Pergunta:

```

```

Predição:

```

```

Por que essa pergunta importa:

```


```

---

## Declaração

Declaramos que nenhum experimento foi executado antes do preenchimento
deste formulário.

Assinaturas: _______________________________________________

Data e hora de envio: __________
