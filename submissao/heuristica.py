"""
SUBMISSÃO — Módulo 1: heurística de busca.

Prazo: 21/09, 23h59. Envie este arquivo junto com submissao/ordenacao.py.

Regras:
  - apenas biblioteca padrão do Python
  - h(cell, mask) deve devolver 0 quando mask está completo e cell é a doca
  - h nunca pode ser negativa
  - não imprima nada, não leia arquivos, não use random sem seed

Antes de enviar, rode:
    python3 verificar_submissao.py <matricula> <curso>
"""

NOME = "COLOQUE O NOME DO GRUPO AQUI"


def make_heuristic(inst):
    """Recebe a instância e devolve a função heurística.

    Faça aqui o pré-processamento caro (uma vez só). A função devolvida
    será chamada centenas de milhares de vezes, então ela precisa ser
    barata.

    O que a instância oferece:
        inst.depot            (linha, coluna) da doca
        inst.items            tupla de 8 posições, na ordem dos bits
        inst.dist[alvo][cel]  distância real (BFS) entre alvo e célula
                              alvos disponíveis: cada item e a doca
        inst.neighbors(cel)   vizinhos livres de uma célula
        inst.grid[l][c]       0 = livre, 1 = prateleira
        inst.free             conjunto de células livres

    Parâmetros de h:
        cell   posição atual do robô
        mask   inteiro de 8 bits; bit i ligado = item i já coletado
    """
    depot = inst.depot
    items = inst.items
    D = inst.dist
    n = len(items)

    def h(cell, mask):
        # EXEMPLO (substitua): máximo sobre itens restantes de
        # distância até o item mais distância do item até a doca.
        melhor = 0
        for i in range(n):
            if not (mask >> i) & 1:
                it = items[i]
                v = D[it][cell] + D[it][depot]
                if v > melhor:
                    melhor = v
        return melhor

    return h
