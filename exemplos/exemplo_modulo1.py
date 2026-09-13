"""
Ponto de partida do Módulo 1. Roda as quatro estratégias de referência na
sua instância e grava dados/modulo1.csv.

    python3 exemplos/exemplo_modulo1.py 20231234 computacao

Isto não é a entrega. É o esqueleto para você adaptar: acrescente sua
heurística, repita execuções, varie o que quiser medir.
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import gen_search
from engine.config import atribuir
from engine.solve_search import astar

matricula, curso = sys.argv[1], sys.argv[2]
seed = atribuir(matricula, curso)["busca"]
inst = gen_search.generate(seed)

sys.path.insert(0, "submissao")
try:
    from heuristica import make_heuristic as minha
except Exception:
    minha = None

configs = [
    ("custo_uniforme", dict(kind="h0")),
    ("astar_manhattan", dict(kind="manhattan")),
    ("astar_real", dict(kind="real")),
    ("gulosa_real", dict(kind="real", greedy=True)),
]
if minha:
    configs.append(("minha_heuristica", dict(kind=minha)))

os.makedirs("dados", exist_ok=True)
linhas = []
for nome, kw in configs:
    r = astar(inst, **kw)
    linhas.append({"seed": seed, "estrategia": nome, "nos_expandidos":
                   r["expanded"], "nos_gerados": r["generated"],
                   "custo": r["cost"], "ms": round(r["ms"], 2)})
    print(f"{nome:>18}  nós={r['expanded']:>7}  custo={r['cost']:>4}  "
          f"{r['ms']:>7.1f}ms")

otimo = min(l["custo"] for l in linhas)
for l in linhas:
    l["razao_otimo"] = round(l["custo"] / otimo, 4)

with open("dados/modulo1.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]))
    w.writeheader(); w.writerows(linhas)
print("\ndados/modulo1.csv gravado")
