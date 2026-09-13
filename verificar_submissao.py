"""
Verifica sua submissão ANTES de enviar.

    python3 verificar_submissao.py <matricula> <curso>

Roda as mesmas checagens do torneio, mas só na sua instância e em mais
duas do pool. Se algo falhar aqui, vai falhar lá.

Este script NÃO diz se sua heurística é boa. Diz se ela é válida.
"""

import argparse
import sys
import time
import traceback

from engine import gen_search, gen_csp
from engine.config import PERFIL, atribuir, carregar_pools
from engine.solve_search import astar
from engine.solve_csp import solve, verify

OK = "  [ok]   "
ERRO = "  [ERRO] "
AVISO = "  [!]    "


def checa_busca(make_h, instancias):
    falhou = False
    for inst in instancias:
        rot = f"seed {inst.seed}"
        try:
            h = make_h(inst)
        except Exception:
            print(ERRO + f"{rot}: make_heuristic lançou exceção")
            traceback.print_exc(limit=2)
            return True

        cheio = (1 << len(inst.items)) - 1
        try:
            hg = h(inst.depot, cheio)
            h0 = h(inst.depot, 0)
        except Exception:
            print(ERRO + f"{rot}: h lançou exceção")
            traceback.print_exc(limit=2)
            return True

        if not isinstance(hg, (int, float)):
            print(ERRO + f"{rot}: h devolveu {type(hg).__name__}, esperado número")
            return True
        if hg != 0:
            print(ERRO + f"{rot}: h(doca, tudo coletado) = {hg}, deveria ser 0")
            falhou = True
        if h0 < 0:
            print(ERRO + f"{rot}: h negativa ({h0})")
            falhou = True

        t0 = time.perf_counter()
        r = astar(inst, make_h)
        dt = time.perf_counter() - t0
        otimo = astar(inst, "h0")["cost"]

        if dt > 20:
            print(ERRO + f"{rot}: {dt:.1f}s, acima do limite de 20s")
            falhou = True
        if r["cost"] != otimo:
            print(AVISO + f"{rot}: custo {r['cost']} contra ótimo {otimo}. "
                          f"Contraexemplo de admissibilidade.")
        else:
            print(OK + f"{rot}: {r['expanded']} nós, custo ótimo ({otimo}), "
                       f"{r['ms']:.0f}ms")
    return falhou


def sonda_consistencia(make_h, inst, amostras=20000):
    import random
    h = make_h(inst)
    ix = {it: i for i, it in enumerate(inst.items)}
    rng = random.Random(0)
    celulas = list(inst.free)
    n = len(inst.items)
    viol = 0
    for _ in range(amostras):
        c = rng.choice(celulas)
        m = rng.randrange(1 << n)
        hc = h(c, m)
        for nb in inst.neighbors(c):
            m2 = m | (1 << ix[nb]) if nb in ix else m
            if hc > 1 + h(nb, m2):
                viol += 1
    return viol


def checa_csp(pick_var, instancias):
    falhou = False
    for inst in instancias:
        rot = f"seed {inst.seed}"
        try:
            a, st = solve(inst, var_order=pick_var, inference="fc",
                          time_limit_s=20)
        except Exception:
            print(ERRO + f"{rot}: pick_var lançou exceção")
            traceback.print_exc(limit=2)
            return True
        if not st.solved:
            print(AVISO + f"{rot}: não terminou em 20s "
                          f"({st.backtracks} backtracks). Será censurada.")
            continue
        if not verify(inst, a):
            print(ERRO + f"{rot}: solução devolvida é inválida")
            falhou = True
            continue
        print(OK + f"{rot}: {st.backtracks} backtracks, {st.ms:.0f}ms")
    return falhou


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("matricula")
    ap.add_argument("curso", choices=sorted(PERFIL))
    args = ap.parse_args()

    sys.path.insert(0, "submissao")
    try:
        import heuristica
        import ordenacao
    except ImportError as e:
        print(f"não consegui importar a submissão: {e}")
        return 1

    for mod, nome in ((heuristica, "heuristica.py"), (ordenacao, "ordenacao.py")):
        n = getattr(mod, "NOME", "")
        if not n or "COLOQUE" in n:
            print(f"{ERRO}{nome}: preencha a variável NOME")
            return 1

    print(f"submissão de: {heuristica.NOME}\n")

    pools = carregar_pools()
    seeds = atribuir(args.matricula, args.curso, pools)

    outros_b = [s for s in pools["busca"][:5] if s != seeds["busca"]][:2]
    inst_b = [gen_search.generate(s) for s in [seeds["busca"]] + outros_b]

    outros_c = [s for s in pools[f"csp_{args.curso}"][:5]
                if s != seeds["csp"]][:2]
    inst_c = [gen_csp.generate(s, **PERFIL[args.curso])
              for s in [seeds["csp"]] + outros_c]

    print("MÓDULO 1 — heurística de busca")
    f1 = checa_busca(heuristica.make_heuristic, inst_b)
    viol = sonda_consistencia(heuristica.make_heuristic, inst_b[0])
    if viol:
        print(AVISO + f"{viol} violações de consistência em 20000 amostras. "
                      f"Isso não invalida a submissão, mas você precisa saber "
                      f"explicar na arguição.")
    else:
        print(OK + "nenhuma violação de consistência na amostra")

    print("\nMÓDULO 2 — ordenação de variáveis")
    f2 = checa_csp(ordenacao.pick_var, inst_c)

    print()
    if f1 or f2:
        print("SUBMISSÃO INVÁLIDA. Corrija os itens marcados com [ERRO].")
        return 1
    print("Submissão válida. Os avisos [!] não impedem o envio.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
