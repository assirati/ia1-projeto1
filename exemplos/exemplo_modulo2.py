"""
Ponto de partida do Módulo 2. Roda as seis células da grade na sua
instância e grava dados/modulo2.csv.

    python3 exemplos/exemplo_modulo2.py 20231234 computacao

Células que não terminarem no limite aparecem com censurada=True. Não
apague essas linhas.
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import gen_csp
from engine.config import PERFIL, atribuir
from engine.solve_csp import solve, verify

matricula, curso = sys.argv[1], sys.argv[2]
LIMITE = 60.0

seed = atribuir(matricula, curso)["csp"]
inst = gen_csp.generate(seed, **PERFIL[curso])
print(f"seed {seed}  carga={inst.tightness():.2f}  "
      f"domínio médio={sum(len(d) for d in inst.domains)/len(inst.domains):.1f}\n")

sys.path.insert(0, "submissao")
try:
    from ordenacao import pick_var as minha
except Exception:
    minha = None

ordenacoes = [("estatica", "static"), ("mrv", "mrv")]
if minha:
    ordenacoes.append(("minha_ordenacao", minha))

os.makedirs("dados", exist_ok=True)
linhas = []
for nome_o, vo in ordenacoes:
    for inf in ("none", "fc", "mac"):
        a, st = solve(inst, var_order=vo, inference=inf, time_limit_s=LIMITE)
        censurada = not st.solved
        linhas.append({"seed": seed, "ordenacao": nome_o, "inferencia": inf,
                       "atribuicoes": st.assignments, "backtracks": st.backtracks,
                       "checks": st.checks, "podas": st.prunings,
                       "ms": round(st.ms, 1), "censurada": censurada,
                       "solucao_valida": verify(inst, a) if a else False})
        marca = "CENSURADA" if censurada else ""
        print(f"{nome_o:>16}/{inf:<5} bt={st.backtracks:>8} "
              f"checks={st.checks:>9} {st.ms:>8.0f}ms {marca}")

with open("dados/modulo2.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]))
    w.writeheader(); w.writerows(linhas)
print("\ndados/modulo2.csv gravado")
