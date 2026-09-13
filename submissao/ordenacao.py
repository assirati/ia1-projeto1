"""
SUBMISSÃO — Módulo 2: heurística de ordenação de variáveis.

Prazo: 21/09, 23h59. Envie junto com submissao/heuristica.py.

Regras:
  - apenas biblioteca padrão do Python
  - deve devolver um índice que esteja em `unassigned`
  - não imprima nada, não leia arquivos

Antes de enviar, rode:
    python3 verificar_submissao.py <matricula> <curso>
"""

NOME = "COLOQUE O NOME DO GRUPO AQUI"


def pick_var(inst, domains, unassigned):
    """Escolhe a próxima variável a ser atribuída.

    O que está disponível:
        inst.trucks[i]        objeto Truck: .dur .earliest .latest .cold .crew
        inst.n_docks          número de docas
        inst.cold_docks       conjunto de docas refrigeradas
        inst.n_slots          número de slots do turno
        inst.related(i, j)    há restrição binária entre i e j?
        inst.conflicts(i, vi, j, vj)   a atribuição viola alguma restrição?
        domains[i]            lista de pares (doca, slot) ainda possíveis
        unassigned            lista de índices ainda não atribuídos

    Você será chamado a cada nó da árvore de busca. Custo importa.
    """
    # EXEMPLO (substitua): MRV puro.
    return min(unassigned, key=lambda i: len(domains[i]))
