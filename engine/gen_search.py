"""
Modulo 1: BUSCA EM ESPACO DE ESTADOS.

Um robo parte da doca, coleta K itens em prateleiras e retorna a doca.
Estado = (celula, bitmask dos itens ja coletados).
Acoes = 4 direcoes, custo unitario.
Objetivo = bitmask completo E estar de volta na doca.

O layout do armazem e FIXO (mesma estrutura de corredores para todos).
O que varia por matricula: posicao da doca, posicao dos K itens e um
conjunto pequeno de travessias bloqueadas.
"""

import random
from collections import deque

W, H = 21, 15
N_ITEMS = 8
N_BLOCKS = 4          # travessias de corredor interditadas


def _base_layout():
    """Prateleiras em blocos, corredores verticais e horizontais."""
    grid = [[0] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            # corredores: linhas 0, 7, 14 e colunas 0, 5, 10, 15, 20
            aisle = (r in (0, 7, H - 1)) or (c in (0, 5, 10, 15, W - 1))
            grid[r][c] = 0 if aisle else 1   # 1 = prateleira
    return grid


BASE = _base_layout()
BASE_FREE = [(r, c) for r in range(H) for c in range(W) if BASE[r][c] == 0]
SHELF_FACES = [
    (r, c) for r in range(H) for c in range(W)
    if BASE[r][c] == 0 and any(
        0 <= r + dr < H and 0 <= c + dc < W and BASE[r + dr][c + dc] == 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
]


class SearchInstance:
    __slots__ = ("grid", "depot", "items", "seed", "free", "dist")

    def __init__(self, grid, depot, items, seed):
        self.grid = grid
        self.depot = depot
        self.items = items
        self.seed = seed
        self.free = {(r, c) for r in range(H) for c in range(W)
                     if grid[r][c] == 0}
        self.dist = {}          # distancias reais a partir de cada alvo

    def neighbors(self, cell):
        r, c = cell
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and self.grid[nr][nc] == 0:
                yield (nr, nc)

    def bfs_from(self, origin):
        d = {origin: 0}
        q = deque([origin])
        while q:
            cur = q.popleft()
            for nb in self.neighbors(cur):
                if nb not in d:
                    d[nb] = d[cur] + 1
                    q.append(nb)
        return d

    def precompute(self):
        for t in list(self.items) + [self.depot]:
            self.dist[t] = self.bfs_from(t)

    def render(self):
        out = []
        idx = {p: str(i) for i, p in enumerate(self.items)}
        for r in range(H):
            row = ""
            for c in range(W):
                p = (r, c)
                if p == self.depot:
                    row += "D"
                elif p in idx:
                    row += idx[p]
                elif self.grid[r][c] == 1:
                    row += "#"
                else:
                    row += "."
            out.append(row)
        return "\n".join(out)


def _connected(grid):
    start = next((r, c) for r in range(H) for c in range(W) if grid[r][c] == 0)
    seen = {start}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] == 0 \
               and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    total = sum(1 for r in range(H) for c in range(W) if grid[r][c] == 0)
    return len(seen) == total


def generate(seed, n_items=N_ITEMS, n_blocks=N_BLOCKS):
    rng = random.Random(seed)
    for _ in range(200):
        grid = [row[:] for row in BASE]
        # interdita travessias sem desconectar o armazem
        candidates = [p for p in BASE_FREE
                      if p[0] not in (0, H - 1) and p[1] not in (0, W - 1)]
        rng.shuffle(candidates)
        blocked = []
        for p in candidates:
            if len(blocked) == n_blocks:
                break
            grid[p[0]][p[1]] = 1
            if _connected(grid):
                blocked.append(p)
            else:
                grid[p[0]][p[1]] = 0
        pool = [p for p in SHELF_FACES if grid[p[0]][p[1]] == 0]
        picks = rng.sample(pool, n_items + 1)
        depot, items = picks[0], tuple(sorted(picks[1:]))
        inst = SearchInstance(grid, depot, items, seed)
        inst.precompute()
        if all(depot in inst.dist[it] for it in items):
            return inst
    raise RuntimeError(f"nao foi possivel gerar instancia para seed {seed}")


def seed_from_matricula(matricula: str) -> int:
    """Determinístico e estável entre execuções (hash() do Python não é)."""
    import hashlib
    h = hashlib.sha256(str(matricula).encode()).hexdigest()
    return int(h[:8], 16)
