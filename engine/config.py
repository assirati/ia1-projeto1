"""
Configuração central. Importado tanto pelas ferramentas do aluno quanto
pelas do professor, para que não haja duas versões da mesma constante.
"""

import hashlib
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Parâmetros do CSP por curso
PERFIL = {
    "producao":   dict(n_trucks=18, n_docks=4, n_crews=5, n_slots=20, window=3),
    "computacao": dict(n_trucks=22, n_docks=3, n_crews=3, n_slots=22, window=2),
}

# Quantas instâncias do pool o torneio usa
N_TORNEIO = 30


def carregar_pools(path=None):
    """Lê a lista de seeds aprovados. O arquivo público não tem baseline."""
    if path is None:
        for nome in ("pools_publico.json", "pools.json"):
            p = os.path.join(RAIZ, nome)
            if os.path.exists(p):
                path = p
                break
    if path is None:
        raise FileNotFoundError(
            "pools_publico.json não encontrado na raiz do repositório")
    return json.load(open(path))["pools"]


def indice(matricula, tag, tamanho):
    h = hashlib.sha256(f"{tag}:{matricula}".encode()).hexdigest()
    return int(h[:12], 16) % tamanho


def atribuir(matricula, curso, pools=None):
    """Seed oficial de cada módulo. Determinístico e auditável."""
    if curso not in PERFIL:
        raise ValueError(f"curso deve ser um de {sorted(PERFIL)}")
    pools = pools or carregar_pools()
    pb = pools["busca"]
    pc = pools[f"csp_{curso}"]
    return {
        "busca": pb[indice(matricula, "busca", len(pb))],
        "csp": pc[indice(matricula, f"csp_{curso}", len(pc))],
    }
