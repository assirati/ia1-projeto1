# Rubrica de Avaliação — Projeto 1

## Como a nota é composta

| Componente                                    | Pontos  | Tipo       |
| --------------------------------------------- | ------- | ---------- |
| 1. Pré-registro de hipóteses                  | 1,5     | grupo      |
| 2. Submissão válida ao torneio de heurísticas | 0,5     | grupo      |
| 3. Pacote reprodutível                        | 1,5     | grupo      |
| 4. Anexo de auditoria de IA                   | 0,5     | grupo      |
| 5. Pôster e análise                           | 2,0     | grupo      |
| 6. Ficha de replicação ao vivo                | 0,5     | grupo      |
| **Subtotal coletivo**                         | **6,5** |            |
| 7. Arguição individual                        | 3,5     | individual |

```
nota final = (subtotal coletivo × multiplicador) + arguição
```

O multiplicador vem da arguição e vale entre 0,5 e 1,0. A tabela está na
seção "O multiplicador", logo depois da seção 7.

---

## 1. Pré-registro de hipóteses — 1,5

Avaliado em 16/09, com nota lançada só depois do pôster. A qualidade da
predição e a qualidade da análise da divergência são avaliadas juntas.

### 1a. Falsificabilidade das predições (0,75)

| Nível        | Pontos | Descritor                                                                                                                                         |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Predições sem número. "A\* será melhor", "MRV vai ajudar"                                                                                         |
| Básico       | 0,25   | Predições com número em menos da metade dos itens obrigatórios, ou faixas tão largas que qualquer resultado cabe (ex.: "entre 1% e 90%")          |
| Proficiente  | 0,5    | Todos os itens obrigatórios com número ou faixa fechada. Justificativas ligam a predição a um mecanismo do algoritmo, não a intuição              |
| Avançado     | 0,75   | Além do acima, ao menos uma predição contraria o resultado esperado do livro-texto e a justificativa explica por que este domínio seria diferente |

**Regra explícita:** predição vaga que acerta pontua **menos** que predição
arriscada que erra. Um grupo que escreveu "A\* expandirá menos nós" e
acertou fica no nível Insuficiente deste critério.

### 1b. Análise da divergência, verificada no pôster (0,75)

| Nível        | Pontos | Descritor                                                                                                     |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | O pôster não menciona o pré-registro, ou trata divergências como erro de medição sem investigar               |
| Básico       | 0,25   | Divergências reportadas, com explicação genérica ("a instância era diferente")                                |
| Proficiente  | 0,5    | Ao menos uma divergência explicada por um mecanismo específico, com o dado que sustenta a explicação apontado |
| Avançado     | 0,75   | Explicação acompanhada de um experimento adicional que discrimina entre duas causas possíveis                 |

---

## 2. Submissão válida ao torneio de heurísticas — 0,5

Binário, com um meio-termo.

| Situação                                                                                                 | Pontos |
| -------------------------------------------------------------------------------------------------------- | ------ |
| Os dois arquivos entregues no prazo, `verificar_submissao.py` passa sem `[ERRO]`, ambos rodam no torneio | 0,5    |
| Um dos dois desqualificado                                                                               | 0,25   |
| Nenhum arquivo válido, ou entrega fora do prazo                                                          | 0      |

**Colocação não pontua.** Uma heurística que fica em último lugar recebe
0,5 desde que seja válida. Uma heurística inadmissível recebe 0,5 desde
que não lance exceção.

O que a heurística faz pela nota aparece nos componentes 5 e 7.

---

## 3. Pacote reprodutível — 1,5

O critério é operacional: o que acontece quando outro grupo roda.

| Nível        | Pontos | Descritor                                                                                                                                 |
| ------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Script não existe, ou não roda nem depois de ajuste                                                                                       |
| Básico       | 0,5    | Roda depois de intervenção manual (corrigir caminho, instalar algo não declarado, editar código)                                          |
| Proficiente  | 1,0    | Roda com um comando, regenera os números do pôster, dados brutos completos e sem filtragem                                                |
| Avançado     | 1,5    | Além do acima: seeds fixados em toda execução aleatória, versões declaradas, e o script falha com mensagem clara se algo estiver faltando |

**Verificação de "sem filtragem":** o CSV do módulo 2 precisa conter as
seis linhas, incluindo as censuradas. Faltar linha de célula que estourou
o tempo derruba para Básico, mesmo que tudo rode.

---

## 4. Anexo de auditoria de IA — 0,5

| Nível        | Pontos | Descritor                                                                                                                             |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Anexo ausente, ou afirma que a IA não errou                                                                                           |
| Básico       | 0,25   | Erro relatado, mas trivial (erro de sintaxe, nome de variável) ou detectado pelo próprio interpretador                                |
| Proficiente  | 0,4    | Erro substantivo, com a descrição de como foi detectado                                                                               |
| Avançado     | 0,5    | Além do acima: o grupo aponta o que teria acontecido se o erro passasse, e descreve a verificação que passaram a fazer por causa dele |

**O que conta como substantivo:** heurística inadmissível apresentada como
admissível, confusão entre admissibilidade e consistência, restrição do CSP
traduzida errado, número plausível que não bateu ao rodar, explicação
confiante e incorreta sobre o comportamento de um algoritmo.

---

## 5. Pôster e análise — 2,0

### 5a. Correção técnica (0,7)

| Nível        | Pontos | Descritor                                                                                                                                                            |
| ------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Erro conceitual central (confunde nós expandidos com gerados, trata busca gulosa como ótima, chama de admissível uma heurística com contraexemplo na própria tabela) |
| Básico       | 0,25   | Sem erro central, mas afirmações imprecisas em pontos secundários                                                                                                    |
| Proficiente  | 0,5    | Terminologia correta, unidades declaradas, comparações feitas entre coisas comparáveis                                                                               |
| Avançado     | 0,7    | Além do acima: o pôster distingue explicitamente o que foi medido do que foi inferido                                                                                |

### 5b. Qualidade da evidência (0,7)

| Nível        | Pontos | Descritor                                                                                                                                   |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Números sem origem rastreável, ou gráfico sem eixo rotulado                                                                                 |
| Básico       | 0,25   | Resultados de execução única, sem menção a variabilidade                                                                                    |
| Proficiente  | 0,5    | Execuções repetidas onde faz sentido, células censuradas reportadas, dados do torneio de heurísticas incorporados                           |
| Avançado     | 0,7    | Além do acima: o grupo identifica uma fonte de variação alheia ao algoritmo (carga da máquina, ordem de execução) e mostra como a controlou |

### 5c. Profundidade da interpretação (0,6)

| Nível        | Pontos | Descritor                                                                                                                         |
| ------------ | ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Tabelas sem leitura. O pôster mostra números e para                                                                               |
| Básico       | 0,2    | Cada resultado acompanhado da explicação padrão de livro-texto                                                                    |
| Proficiente  | 0,4    | Ao menos um resultado explicado por uma característica específica desta instância ou deste domínio                                |
| Avançado     | 0,6    | O grupo compara o desempenho da própria heurística na própria instância com o desempenho na média da turma, e explica a diferença |

---

## 6. Ficha de replicação ao vivo — 0,5

Preenchida em 28/09 pelo grupo auditor.

| Nível        | Pontos | Descritor                                                                                                              |
| ------------ | ------ | ---------------------------------------------------------------------------------------------------------------------- |
| Insuficiente | 0      | Ficha sem evidência de que o script foi rodado (campos de valor regenerado vazios ou idênticos ao pôster sem execução) |
| Básico       | 0,25   | Ficha completa, três números conferidos, nada além disso                                                               |
| Proficiente  | 0,4    | Além do acima: a pergunta do campo 4 é sobre algo que só se percebe rodando o código                                   |
| Avançado     | 0,5    | O auditor encontra uma divergência real, ou uma afirmação não sustentada pelos dados brutos, e a descreve com precisão |

**Penalidade cruzada.** Se o professor detectar depois um erro grave que o
auditor deixou passar, ambos os grupos perdem 0,25: o auditor neste
componente, o auditado no componente 3.

---

## 7. Arguição individual — 3,5

Três perguntas, 6 a 8 minutos. Duas sorteadas do banco público, uma
improvisada a partir do pôster e dos dados do grupo.

### Pontuação por pergunta

Cada uma vale até 1,17, e a soma das três é limitada a 3,5. Escala
aplicada individualmente:

| Nível        | Fração | Descritor                                                                                                                                               |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Não responde | 0      | Silêncio, ou resposta que não trata da pergunta                                                                                                         |
| Recita       | 0,25   | Reproduz a definição correta sem conectá-la ao trabalho do grupo                                                                                        |
| Aplica       | 0,6    | Conecta o conceito ao próprio trabalho, apontando o dado ou o trecho de código relevante                                                                |
| Domina       | 1,0    | Além do acima: reconhece o limite da própria resposta, ou constrói um contraexemplo, ou prevê corretamente o resultado de uma variação proposta na hora |

### Sobre a terceira pergunta

Ela é o discriminante do projeto. Formatos:

> "Sua heurística ficou em 4º na sua instância e em 15º na média da turma.
> O que isso diz?"

> "Muda esse parâmetro e roda. O que você espera antes de apertar enter?"

> "Por que a instância de vocês expandiu 2.100 nós e a do grupo ao lado
> expandiu 700, com a mesma heurística?"

Quem produziu os dados responde. Quem recebeu os resultados prontos, não.

### Condições de avaliação

Respostas podem ser dadas apontando para o pôster, escrevendo no papel ou
rodando código na hora. Avalia-se o conteúdo, não a desenvoltura.

Hesitação, gagueira e nervosismo não descontam. Uma resposta correta dita
mal vale o mesmo que uma resposta correta dita bem.

---

## O multiplicador

A nota da arguição também determina um multiplicador aplicado aos 6,5
pontos coletivos.

| Arguição                 | Multiplicador |
| ------------------------ | ------------- |
| 3,0 ou mais              | 1,00          |
| de 2,3 a menos de 3,0    | 0,90          |
| de 1,5 a menos de 2,3    | 0,75          |
| de 0,8 a menos de 1,5    | 0,60          |
| abaixo de 0,8            | 0,50          |

**Por que isso existe.** Quem não consegue explicar o próprio trabalho não
carrega a nota do grupo. O mecanismo resolve o problema do carona sem
exigir que ninguém denuncie ninguém.

**Exemplo.** Grupo com 5,8 de subtotal coletivo:

| Aluno | Arguição | Multiplicador | Nota final       |
| ----- | -------- | ------------- | ---------------- |
| A     | 3,2      | 1,00          | 5,8 + 3,2 = 9,0  |
| B     | 2,5      | 0,90          | 5,22 + 2,5 = 7,7 |
| C     | 1,0      | 0,60          | 3,48 + 1,0 = 4,5 |

---

## Prazos e penalidades

| Entrega                      | Prazo            | Atraso                        |
| ---------------------------- | ---------------- | ----------------------------- |
| Pré-registro                 | 16/09, 23h59     | Não aceito. Componente zerado |
| Submissão ao torneio         | 21/09, 23h59     | Não aceito. Componente zerado |
| Pacote reprodutível e pôster | 26/09, 23h59     | Não aceito. Componente zerado |
| Ficha de replicação          | 28/09, na sessão | Não aceito fora da sessão     |

Nenhum prazo tem tolerância. O pré-registro depende de ser anterior à
execução, e o torneio é uma execução coletiva única: não há como rodá-lo
de novo para quem perdeu a data.
