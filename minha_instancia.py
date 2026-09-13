"""
Entrega a instância oficial do seu grupo.

    python3 minha_instancia.py 20231234 computacao
    python3 minha_instancia.py 20231234 computacao --json

Use a matrícula do integrante mais velho. O mapeamento matrícula -> seed é
determinístico: a lista de seeds aprovados está em pools_publico.json e a
função de índice está em engine/config.py. Não há aleatoriedade oculta.
"""

import argparse
import json

from engine import gen_search, gen_csp
from engine.config import PERFIL, atribuir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("matricula")
    ap.add_argument("curso", choices=sorted(PERFIL))
    ap.add_argument("--json", action="store_true",
                    help="grava dados/instancia_<matricula>.json")
    args = ap.parse_args()

    seeds = atribuir(args.matricula, args.curso)
    inst_b = gen_search.generate(seeds["busca"])
    inst_c = gen_csp.generate(seeds["csp"], **PERFIL[args.curso])

    print(f"matrícula {args.matricula}  |  curso {args.curso}")
    print(f"seed busca = {seeds['busca']}   seed csp = {seeds['csp']}")
    print("\n=== MÓDULO 1: rota de coleta ===")
    print("D = doca (início e fim), 0..7 = itens, # = prateleira\n")
    print(inst_b.render())
    print("\n=== MÓDULO 2: alocação de docas ===")
    print(inst_c.describe())

    if args.json:
        payload = {
            "matricula": args.matricula, "curso": args.curso, "seeds": seeds,
            "busca": {"largura": gen_search.W, "altura": gen_search.H,
                      "grid": inst_b.grid, "doca": list(inst_b.depot),
                      "itens": [list(p) for p in inst_b.items]},
            "csp": {"n_docas": inst_c.n_docks,
                    "docas_frias": sorted(inst_c.cold_docks),
                    "n_slots": inst_c.n_slots,
                    "caminhoes": [
                        {"id": t.tid, "duracao": t.dur, "mais_cedo": t.earliest,
                         "mais_tarde": t.latest, "refrigerado": t.cold,
                         "equipe": t.crew} for t in inst_c.trucks]},
        }
        out = f"dados/instancia_{args.matricula}.json"
        json.dump(payload, open(out, "w"), indent=1)
        print(f"\ngravado em {out}")


if __name__ == "__main__":
    main()
