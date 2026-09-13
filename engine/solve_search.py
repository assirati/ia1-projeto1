"""
Solvers de referencia para o Modulo 1. Todos contam nos expandidos.

Heuristicas disponiveis:
  h0        : zero (reduz A* a Dijkstra / busca de custo uniforme)
  manhattan : max sobre itens restantes de (manh(cur,i) + manh(i,depot))
  real      : idem, com distancias reais pre-computadas por BFS
  mst       : real + arvore geradora minima sobre os itens restantes

Admissibilidade de 'manhattan' e 'real': para terminar e preciso visitar
cada item restante i e depois voltar a doca, logo o custo restante e no
minimo d(cur,i) + d(i,depot) para QUALQUER i restante. O maximo desses
limites continua sendo um limite inferior.
"""

import heapq
import itertools
import time


def manh(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def make_heuristic(inst, kind):
    """kind pode ser um nome de referencia ou uma fabrica submetida pelo grupo:
    uma funcao make(inst) -> h(cell, mask) -> int."""
    if callable(kind):
        return kind(inst)

    depot, items = inst.depot, inst.items
    n = len(items)

    if kind == "h0":
        return lambda cell, mask: 0

    if kind == "manhattan":
        def h(cell, mask):
            best = 0
            for i in range(n):
                if not (mask >> i) & 1:
                    it = items[i]
                    v = manh(cell, it) + manh(it, depot)
                    if v > best:
                        best = v
            return best
        return h

    D = inst.dist

    if kind == "real":
        def h(cell, mask):
            best = 0
            for i in range(n):
                if not (mask >> i) & 1:
                    it = items[i]
                    v = D[it][cell] + D[it][depot]
                    if v > best:
                        best = v
            return best
        return h

    if kind == "mst":
        def h(cell, mask):
            rem = [items[i] for i in range(n) if not (mask >> i) & 1]
            if not rem:
                return D[depot][cell]
            # entrada mais barata na arvore + MST dos restantes + saida
            entry = min(D[it][cell] for it in rem)
            exit_ = min(D[it][depot] for it in rem)
            # Prim sobre distancias reais entre itens
            in_tree = {rem[0]}
            cost = 0
            while len(in_tree) < len(rem):
                best, best_node = None, None
                for out in rem:
                    if out in in_tree:
                        continue
                    d = min(D[out][t] for t in in_tree)
                    if best is None or d < best:
                        best, best_node = d, out
                in_tree.add(best_node)
                cost += best
            return entry + cost + exit_
        return h

    raise ValueError(kind)


def astar(inst, kind="real", greedy=False, weight=1.0):
    """Retorna dict com custo, nos expandidos, nos gerados e tempo."""
    h = make_heuristic(inst, kind)
    start = (inst.depot, 0)
    full = (1 << len(inst.items)) - 1
    item_ix = {it: i for i, it in enumerate(inst.items)}

    t0 = time.perf_counter()
    counter = itertools.count()
    g = {start: 0}
    h0 = h(inst.depot, 0)
    # Sem conjunto fechado. Uma heuristica admissivel porem INCONSISTENTE
    # exige reabertura de nos; com closed set e sem reabrir, A* pode
    # devolver solucao subotima. Entradas obsoletas na fila sao
    # descartadas pela comparacao de g.
    pq = [(h0 if greedy else h0 * weight, next(counter), start, 0)]
    expanded = generated = 0

    while pq:
        _, _, state, gs = heapq.heappop(pq)
        if gs > g.get(state, float("inf")):
            continue
        expanded += 1
        cell, mask = state
        if mask == full and cell == inst.depot:
            return {"cost": gs, "expanded": expanded,
                    "generated": generated,
                    "ms": (time.perf_counter() - t0) * 1000,
                    "solved": True}
        ng = gs + 1
        for nb in inst.neighbors(cell):
            nmask = mask
            if nb in item_ix:
                nmask |= 1 << item_ix[nb]
            ns = (nb, nmask)
            if ns in g and g[ns] <= ng:
                continue
            g[ns] = ng
            generated += 1
            hv = h(nb, nmask)
            f = hv if greedy else ng + weight * hv
            heapq.heappush(pq, (f, next(counter), ns, ng))
    return {"cost": None, "expanded": expanded, "generated": generated,
            "ms": (time.perf_counter() - t0) * 1000, "solved": False}
