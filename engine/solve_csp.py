"""
Solver de referencia para o Modulo 2.

Eixos configuraveis (a grade fatorial que os grupos devem varrer):
  var_order : 'static' | 'mrv' | 'mrv_deg'
  val_order : 'static' | 'lcv'
  inference : 'none' | 'fc' | 'mac'   (mac = AC-3 apos cada atribuicao)

Metricas: atribuicoes, backtracks, verificacoes de restricao, tempo.
"""

import time
from collections import deque


class Stats:
    __slots__ = ("assignments", "backtracks", "checks", "ms", "solved",
                 "prunings")

    def __init__(self):
        self.assignments = 0
        self.backtracks = 0
        self.checks = 0
        self.prunings = 0
        self.ms = 0.0
        self.solved = False

    def as_dict(self):
        return {"assignments": self.assignments, "backtracks": self.backtracks,
                "checks": self.checks, "prunings": self.prunings,
                "ms": round(self.ms, 1), "solved": self.solved}


def _revise(inst, domains, xi, xj, st):
    removed = []
    for vi in domains[xi]:
        st.checks += 1
        if not any(not inst.conflicts(xi, vi, xj, vj) for vj in domains[xj]):
            removed.append(vi)
    if removed:
        domains[xi] = [v for v in domains[xi] if v not in set(removed)]
        st.prunings += len(removed)
    return removed


def _ac3(inst, domains, st, queue=None):
    n = len(inst.trucks)
    if queue is None:
        queue = deque((i, j) for i in range(n) for j in range(n)
                      if i != j and inst.related(i, j))
    else:
        queue = deque(queue)
    while queue:
        xi, xj = queue.popleft()
        if _revise(inst, domains, xi, xj, st):
            if not domains[xi]:
                return False
            for xk in range(n):
                if xk != xi and xk != xj and inst.related(xk, xi):
                    queue.append((xk, xi))
    return True


def _forward_check(inst, domains, var, val, unassigned, st):
    for other in unassigned:
        if not inst.related(var, other):
            continue
        kept = []
        for v in domains[other]:
            st.checks += 1
            if not inst.conflicts(var, val, other, v):
                kept.append(v)
        if len(kept) != len(domains[other]):
            st.prunings += len(domains[other]) - len(kept)
            domains[other] = kept
        if not kept:
            return False
    return True


def _pick_var(inst, domains, unassigned, mode):
    if callable(mode):
        v = mode(inst, domains, unassigned)
        if v not in unassigned:
            raise ValueError(f"ordenacao devolveu variavel invalida: {v!r}")
        return v
    if mode == "static":
        return unassigned[0]
    if mode == "mrv":
        return min(unassigned, key=lambda i: len(domains[i]))
    if mode == "mrv_deg":
        deg = {i: sum(1 for j in unassigned if j != i and inst.related(i, j))
               for i in unassigned}
        return min(unassigned, key=lambda i: (len(domains[i]), -deg[i]))
    raise ValueError(mode)


def _order_vals(inst, domains, var, unassigned, mode, st):
    if mode == "static":
        return list(domains[var])
    scored = []
    for v in domains[var]:
        loss = 0
        for other in unassigned:
            if other == var or not inst.related(var, other):
                continue
            for w in domains[other]:
                st.checks += 1
                if inst.conflicts(var, v, other, w):
                    loss += 1
        scored.append((loss, v))
    scored.sort()
    return [v for _, v in scored]


def solve(inst, var_order="static", val_order="static", inference="none",
          time_limit_s=30.0):
    st = Stats()
    n = len(inst.trucks)
    domains = [list(d) for d in inst.domains]
    t0 = time.perf_counter()

    if inference == "mac":
        if not _ac3(inst, domains, st):
            st.ms = (time.perf_counter() - t0) * 1000
            return None, st

    assignment = {}

    def backtrack():
        if time.perf_counter() - t0 > time_limit_s:
            raise TimeoutError
        if len(assignment) == n:
            return True
        unassigned = [i for i in range(n) if i not in assignment]
        var = _pick_var(inst, domains, unassigned, var_order)
        rest = [u for u in unassigned if u != var]
        for val in _order_vals(inst, domains, var, rest, val_order, st):
            ok = True
            for other, oval in assignment.items():
                st.checks += 1
                if inst.conflicts(var, val, other, oval):
                    ok = False
                    break
            if not ok:
                continue
            assignment[var] = val
            st.assignments += 1
            saved = [list(d) for d in domains]
            domains[var] = [val]
            good = True
            if inference == "fc":
                good = _forward_check(inst, domains, var, val, rest, st)
            elif inference == "mac":
                q = [(o, var) for o in rest if inst.related(o, var)]
                good = _ac3(inst, domains, st, q)
                if good and any(not domains[u] for u in rest):
                    good = False
            if good and backtrack():
                return True
            for i in range(n):
                domains[i] = saved[i]
            del assignment[var]
            st.backtracks += 1
        return False

    try:
        found = backtrack()
    except TimeoutError:
        st.ms = (time.perf_counter() - t0) * 1000
        return None, st

    st.ms = (time.perf_counter() - t0) * 1000
    st.solved = found
    return (dict(assignment) if found else None), st


def verify(inst, assignment):
    if assignment is None or len(assignment) != len(inst.trucks):
        return False
    for i, vi in assignment.items():
        if vi not in inst.domains[i]:
            return False
        for j, vj in assignment.items():
            if i < j and inst.conflicts(i, vi, j, vj):
                return False
    return True
