# Banco Público de Perguntas — Arguição

Vinte e quatro perguntas. **Duas serão sorteadas** para cada aluno no dia.
A terceira será improvisada a partir do seu pôster e não está aqui. Estudem.

Várias perguntas pedem que vocês olhem para os **seus** números. Tenham o
pôster e o notebook à mão.

---

## Módulo 1 — Busca em espaço de estados

**1.1** Por que o estado deste problema precisa incluir o conjunto de itens
já coletados? O que aconteceria se o estado fosse apenas a posição do robô?

**1.2** Estime o tamanho do espaço de estados da sua instância e compare
com o número de nós que o custo uniforme expandiu. Por que a diferença?

**1.3** O que significa uma heurística ser admissível? Dê um exemplo, neste
problema, de heurística inadmissível que ainda assim seria útil.

**1.4** Admissível e consistente não são a mesma coisa. Explique a
diferença e diga o que A\* precisa fazer de diferente quando a heurística é
admissível mas inconsistente.

**1.5** A heurística de distância real usa BFS pré-computada a partir de
cada item. Essa pré-computação conta como custo do algoritmo? Justifique
dos dois lados.

**1.6** Na sua instância, a busca gulosa expandiu muito menos nós e
devolveu rota pior. Explique o mecanismo, apontando o que o guloso ignora.

**1.7** Descreva sua heurística. Ela é admissível? Consistente? Mostre o
argumento, não apenas a conclusão.

**1.8** Suponha que o robô ganhe uma quinta ação: teletransporte para a
doca, com custo 15. Sua heurística continua admissível? O que muda no
espaço de estados?

**1.9** Dois grupos com a mesma heurística obtiveram contagens de nós muito
diferentes. Cite duas características da instância que poderiam explicar
isso e diga como você testaria cada uma.

**1.10** Por que a heurística de máximo é admissível e a de soma das
distâncias não é? Construa o contraexemplo.

---

## Módulo 2 — Satisfação de restrições

**2.1** Escreva formalmente a restrição binária entre dois caminhões que
compartilham doca. Por que ela não é simplesmente "docas diferentes"?

**2.2** A restrição de equipe e a de doca se parecem, mas se comportam
diferente na propagação. Explique a diferença.

**2.3** O que forward checking faz que o backtracking cronológico não faz?
Descreva o momento exato em que a poda ocorre.

**2.4** Explique AC-3 em termos do que a fila contém e de quando um arco
volta para a fila. Por que revisar um arco pode exigir reenfileirar outros?

**2.5** Nos seus dados, MRV sozinho e forward checking sozinho tiveram
desempenhos muito diferentes. Qual venceu, por qual fator, e por quê? Isso
bateu com sua predição?

**2.6** MAC faz mais verificações de restrição que forward checking e ainda
assim pode terminar antes. Explique o trade-off usando os seus números.

**2.7** Você reportou alguma célula como censurada. O que exatamente
significa esse dado, e por que omiti-lo distorceria a comparação?

**2.8** Todas as instâncias têm solução, por construção. Se uma fosse
insatisfatível, o que aconteceria com cada uma das seis configurações? Qual
detectaria mais rápido, e por quê?

**2.9** Descreva sua heurística de ordenação de variáveis e diga em que
situação ela deve perder para MRV puro.

**2.10** O gerador planta uma solução viável e deriva as janelas de tempo
em torno dela. Isso torna as instâncias mais fáceis do que instâncias
aleatórias com a mesma carga? Argumente dos dois lados.

---

## Torneio de heurísticas

**3.1** Sua heurística teve desempenho diferente na sua instância e na
média da turma. Quantifique a diferença e explique a causa.

**3.2** A tabela reporta "sem contraexemplo em 30 instâncias" em vez de
"admissível". Por que essa distinção importa?

**3.3** Uma heurística inadmissível apareceu bem colocada em nós
expandidos. Em que situação real você aceitaria usá-la, e o que exigiria
antes de aceitar?

**3.4** Escolha uma heurística de outro grupo que superou a sua. Explique o
que ela captura que a sua não captura.

---

## Transversais

**T.1** Aponte, no seu pôster, o resultado que mais contrariou sua
predição. O que você faria diferente com mais uma semana?

**T.2** Descreva o erro de IA generativa que vocês documentaram no anexo.
Como foi detectado, e o que teria acontecido se não fosse?

**T.3** Uma afirmação do seu pôster que os dados brutos sustentam menos do
que parece. Qual é, e o que faltaria medir?

**T.4** Seu grupo mediu tempo de execução. Cite duas fontes de variação
nessa medida que nada têm a ver com o algoritmo, e diga como vocês as
controlaram.
