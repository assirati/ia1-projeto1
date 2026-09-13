"""
Modulo 2: SATISFACAO DE RESTRICOES.

Alocar N caminhoes a docas e horarios de inicio.

Variavel  : um caminhao
Dominio   : pares (doca, slot_inicial)
Restricoes:
  unarias  - janela de tempo do caminhao; caminhao refrigerado exige doca fria
  binarias - dois caminhoes na MESMA doca nao podem se sobrepor no tempo
             dois caminhoes da MESMA equipe nao podem se sobrepor no tempo

Todas as restricoes binarias sao pares, o que mantem AC-3 aplicavel sem
adaptacao. As unarias sao dobradas no dominio inicial.
"""

import hashlib
import random

N_TRUCKS = 16
N_DOCKS = 4
COLD_DOCKS = (0, 1)
N_SLOTS = 20          # slots de 30 min -> jornada de 10h
N_CREWS = 5


class Truck:
    __slots__ = ("tid", "dur", "earliest", "latest", "cold", "crew")

    def __init__(self, tid, dur, earliest, latest, cold, crew):
        self.tid = tid
        self.dur = dur
        self.earliest = earliest
        self.latest = latest      # ultimo slot de INICIO permitido
        self.cold = cold
        self.crew = crew

    def __repr__(self):
        return (f"T{self.tid}(dur={self.dur}, janela=[{self.earliest},"
                f"{self.latest}], frio={int(self.cold)}, eq={self.crew})")


class CSPInstance:
    def __init__(self, trucks, n_docks, cold_docks, n_slots, seed):
        self.trucks = trucks
        self.n_docks = n_docks
        self.cold_docks = set(cold_docks)
        self.n_slots = n_slots
        self.seed = seed
        self.domains = [self._init_domain(t) for t in trucks]

    def _init_domain(self, t):
        docks = sorted(self.cold_docks) if t.cold else range(self.n_docks)
        return [(d, s) for d in docks
                for s in range(t.earliest, min(t.latest, self.n_slots - t.dur) + 1)]

    def conflicts(self, i, vi, j, vj):
        """True se a atribuicao dos caminhoes i e j viola alguma restricao."""
        ti, tj = self.trucks[i], self.trucks[j]
        di, si = vi
        dj, sj = vj
        overlap = si < sj + tj.dur and sj < si + ti.dur
        if not overlap:
            return False
        if di == dj:
            return True
        if ti.crew == tj.crew:
            return True
        return False

    def related(self, i, j):
        """Ha alguma restricao binaria entre i e j?"""
        ti, tj = self.trucks[i], self.trucks[j]
        if ti.crew == tj.crew:
            return True
        di = self.cold_docks if ti.cold else set(range(self.n_docks))
        dj = self.cold_docks if tj.cold else set(range(self.n_docks))
        return bool(di & dj)

    def tightness(self):
        load = sum(t.dur for t in self.trucks)
        return load / (self.n_docks * self.n_slots)

    def describe(self):
        lines = [f"seed={self.seed}  docas={self.n_docks} "
                 f"(frias={sorted(self.cold_docks)})  slots={self.n_slots}",
                 f"carga/capacidade = {self.tightness():.2f}",
                 f"tamanho medio de dominio = "
                 f"{sum(len(d) for d in self.domains)/len(self.domains):.1f}"]
        lines += ["  " + repr(t) for t in self.trucks]
        return "\n".join(lines)


def generate(seed, n_trucks=N_TRUCKS, n_docks=N_DOCKS, n_slots=N_SLOTS,
             n_crews=N_CREWS, cold_docks=COLD_DOCKS, window=5):
    """
    Gera por SOLUCAO PLANTADA: primeiro monta uma escala viavel, depois
    deriva as janelas em torno dela. Garante ao menos uma solucao e evita
    que a turma receba instancias insatisfativeis por acidente.

    'window' controla a folga: menor = mais restrito = mais backtracks.
    """
    rng = random.Random(seed ^ 0x5EED)
    cold_docks = tuple(cold_docks)

    for _ in range(400):
        dock_busy = {d: [] for d in range(n_docks)}
        crew_busy = {c: [] for c in range(n_crews)}
        planted = []
        ok = True
        order = list(range(n_trucks))
        rng.shuffle(order)
        for _tid in order:
            dur = rng.choice([2, 2, 3, 3, 4])
            cold = rng.random() < 0.30
            docks = list(cold_docks) if cold else list(range(n_docks))
            slots = []
            for d in docks:
                for c in range(n_crews):
                    for s in range(n_slots - dur + 1):
                        if any(s < b + bd and b < s + dur
                               for b, bd in dock_busy[d]):
                            continue
                        if any(s < b + bd and b < s + dur
                               for b, bd in crew_busy[c]):
                            continue
                        slots.append((d, c, s))
            if not slots:
                ok = False
                break
            d, c, s = rng.choice(slots)
            dock_busy[d].append((s, dur))
            crew_busy[c].append((s, dur))
            planted.append((dur, cold, c, s))
        if not ok:
            continue

        trucks = []
        for tid, (dur, cold, crew, s) in enumerate(planted):
            back = rng.randint(0, window)
            fwd = window - back
            earliest = max(0, s - back)
            latest = min(n_slots - dur, s + fwd)
            trucks.append(Truck(tid, dur, earliest, latest, cold, crew))
        return CSPInstance(trucks, n_docks, cold_docks, n_slots, seed)

    raise RuntimeError(f"nao foi possivel plantar solucao para seed {seed}")


def seed_from_matricula(matricula: str) -> int:
    h = hashlib.sha256(("csp:" + str(matricula)).encode()).hexdigest()
    return int(h[:8], 16)
