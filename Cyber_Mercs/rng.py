# rng.py — Motor de probabilidades para Cyber-Mercs
# Centraliza: afinidad clase/contrato, eventos, HP modifier, implantes mecánicos.
# Ni main.py ni agente.py tocan probabilidades directamente — todo pasa por aquí.

import random
from dataclasses import dataclass

# ──────────────────────────────────────────────────────────────────
# 1. Afinidad Clase ↔ Tipo de Contrato
# ──────────────────────────────────────────────────────────────────

AFINIDAD: dict[str, dict[str, str]] = {
    "hacker": {
        "hackeo": "fuerte",
        "infiltracion": "fuerte",
        "sabotaje": "neutral",
        "asalto": "debil",
        "combate": "debil",
    },
    "tanque": {
        "asalto": "fuerte",
        "combate": "fuerte",
        "sabotaje": "neutral",
        "hackeo": "debil",
        "infiltracion": "debil",
    },
    "sniper": {
        "infiltracion": "fuerte",
        "sabotaje": "neutral",
        "hackeo": "neutral",
        "combate": "neutral",
        "asalto": "debil",
    },
    "fixer": {
        "sabotaje": "fuerte",
        "hackeo": "fuerte",
        "infiltracion": "neutral",
        "asalto": "debil",
        "combate": "debil",
    },
    "novato": {
        "hackeo": "neutral",
        "infiltracion": "neutral",
        "sabotaje": "neutral",
        "asalto": "neutral",
        "combate": "neutral",
    },
}


def obtener_afinidad(clase: str, tipo_contrato: str) -> str:
    """Retorna 'fuerte', 'neutral' o 'debil'."""
    return AFINIDAD.get(clase, AFINIDAD["novato"]).get(tipo_contrato, "neutral")


# ──────────────────────────────────────────────────────────────────
# 2. Tabla de 7 Eventos
# ──────────────────────────────────────────────────────────────────

@dataclass
class EventoRNG:
    """Resultado de una tirada del motor RNG."""
    nombre: str
    multiplicador_dano: float
    multiplicador_pago: float
    implante_garantizado: bool = False
    implante_boost: bool = False      # +30% chance (90% total)
    mision_fallida: bool = False


# Definición de los 7 eventos (ordenados de mejor a peor)
EVENTOS = {
    "jackpot":      EventoRNG("Jackpot Corporativo",      0.0, 2.0, implante_garantizado=True),
    "suerte":       EventoRNG("Golpe de Suerte",           0.0, 1.0, implante_boost=True),
    "fantasma":     EventoRNG("Infiltración Fantasma",     0.5, 1.0),
    "limpia":       EventoRNG("Operación Limpia",          1.0, 1.0),
    "resistencia":  EventoRNG("Resistencia Inesperada",    1.25, 1.0),
    "emboscada":    EventoRNG("Emboscada Corporativa",     1.5, 1.0),
    "desastre":     EventoRNG("Desastre Absoluto",         2.0, 0.0, mision_fallida=True),
}

# Orden de las keys para indexar las distribuciones
_ORDEN = ["jackpot", "suerte", "fantasma", "limpia", "resistencia", "emboscada", "desastre"]

# ──────────────────────────────────────────────────────────────────
# 3. Distribuciones por Afinidad (pesos, no porcentajes fijos)
# ──────────────────────────────────────────────────────────────────

DISTRIBUCIONES: dict[str, list[int]] = {
    #              jackpot  suerte  fantasma  limpia  resistencia  emboscada  desastre
    "fuerte":  [    10,      20,      25,      25,       10,          8,        2  ],
    "neutral": [     5,      10,      20,      30,       15,         15,        5  ],
    "debil":   [     2,       8,      10,      25,       20,         25,       10  ],
}


# ──────────────────────────────────────────────────────────────────
# 4. Modificador por HP
# ──────────────────────────────────────────────────────────────────

def _degradar_afinidad(afinidad: str) -> str:
    """Baja un nivel: fuerte→neutral, neutral→debil, debil→debil."""
    if afinidad == "fuerte":
        return "neutral"
    return "debil"


def afinidad_con_hp(afinidad_base: str, hp_actual: int, hp_max: int) -> str:
    """Aplica el modificador por estado físico del mercenario.
    - HP > 60%: sin cambio
    - HP 30-60%: baja un nivel
    - HP < 30%: siempre débil"""
    if hp_max <= 0:
        return "debil"
    ratio = hp_actual / hp_max
    if ratio > 0.6:
        return afinidad_base
    if ratio >= 0.3:
        return _degradar_afinidad(afinidad_base)
    return "debil"


# ──────────────────────────────────────────────────────────────────
# 5. Efectos mecánicos de implantes
# ──────────────────────────────────────────────────────────────────

# Mapa: nombre_implante → (tipos_contrato donde aplica, efecto)
IMPLANTE_PROTECCION: dict[str, tuple[set[str], str]] = {
    "Brazo Biónico de Titanio":  ({"asalto", "combate"}, "reduce_5"),
    "Subdermal Armor v2":        (set(), "reduce_3"),          # aplica siempre
    "Ojo Óptico Kiroshi":        ({"infiltracion"}, "salva_desastre"),
    "Neuro-Enlace Cuántico":     ({"hackeo"}, "salva_desastre"),
    "Piernas Neumáticas":        (set(), "escape_50"),         # aplica siempre
}


def aplicar_implantes_al_evento(
    evento_key: str,
    tipo_contrato: str,
    implantes: list[str],
) -> str:
    """Si el mercenario tiene implantes relevantes, puede convertir un Desastre
    en Emboscada o un escape. Retorna la key del evento final."""
    if evento_key != "desastre":
        return evento_key

    for implante in implantes:
        spec = IMPLANTE_PROTECCION.get(implante)
        if spec is None:
            continue
        tipos_aplica, efecto = spec

        if efecto == "salva_desastre":
            if tipo_contrato in tipos_aplica:
                return "emboscada"  # Desastre → Emboscada

        if efecto == "escape_50":
            if random.random() < 0.5:
                return "resistencia"  # Desastre → Resistencia (escapó)

    return evento_key


def reduccion_dano_implantes(tipo_contrato: str, implantes: list[str]) -> int:
    """Retorna la reducción de daño fijo por implantes equipados."""
    reduccion = 0
    for implante in implantes:
        spec = IMPLANTE_PROTECCION.get(implante)
        if spec is None:
            continue
        tipos_aplica, efecto = spec
        if efecto == "reduce_5" and (not tipos_aplica or tipo_contrato in tipos_aplica):
            reduccion += 5
        elif efecto == "reduce_3":
            reduccion += 3
    return reduccion


# ──────────────────────────────────────────────────────────────────
# 6. Motor principal — Modo Autónomo (sin dado)
# ──────────────────────────────────────────────────────────────────

def resolver_evento_autonomo(
    clase: str,
    tipo_contrato: str,
    hp_actual: int,
    hp_max: int,
    implantes: list[str] | None = None,
) -> EventoRNG:
    """Resuelve un evento completo para el modo autónomo (cliente.py).
    1. Calcula afinidad base (clase vs contrato)
    2. Aplica degradación por HP
    3. Tira RNG con la distribución correcta
    4. Aplica efectos de implantes
    5. Retorna el EventoRNG final"""
    implantes = implantes or []

    # Afinidad
    afinidad_base = obtener_afinidad(clase, tipo_contrato)
    afinidad_final = afinidad_con_hp(afinidad_base, hp_actual, hp_max)

    # Tirada con pesos
    pesos = DISTRIBUCIONES[afinidad_final]
    evento_key = random.choices(_ORDEN, weights=pesos, k=1)[0]

    # Implantes pueden salvar de un desastre
    evento_key = aplicar_implantes_al_evento(evento_key, tipo_contrato, implantes)

    return EVENTOS[evento_key]


# ──────────────────────────────────────────────────────────────────
# 7. Motor D20 — Modo Interactivo (con dado)
# ──────────────────────────────────────────────────────────────────

UMBRALES_D20: dict[str, dict[str, int]] = {
    #                perfecto  estandar (>= X éxito, < X emboscada)
    "fuerte":  {"perfecto": 12, "estandar": 7},
    "neutral": {"perfecto": 15, "estandar": 10},
    "debil":   {"perfecto": 18, "estandar": 13},
}


def resolver_evento_d20(
    tirada: int,
    clase: str,
    tipo_contrato: str,
    hp_actual: int,
    hp_max: int,
    implantes: list[str] | None = None,
) -> EventoRNG:
    """Resuelve un evento para el modo interactivo (clienteInteractivo.py).
    Usa la tirada D20 del usuario + umbrales dinámicos por afinidad."""
    implantes = implantes or []

    afinidad_base = obtener_afinidad(clase, tipo_contrato)
    afinidad_final = afinidad_con_hp(afinidad_base, hp_actual, hp_max)

    umbrales = UMBRALES_D20[afinidad_final]

    if tirada >= umbrales["perfecto"]:
        # Perfecto: elegir entre jackpot (nat 20) y suerte/fantasma
        if tirada == 20:
            evento_key = "jackpot"
        else:
            evento_key = random.choice(["suerte", "fantasma"])
    elif tirada >= umbrales["estandar"]:
        evento_key = random.choice(["limpia", "resistencia"])
    else:
        # Fallo: elegir entre emboscada y desastre (nat 1)
        if tirada == 1:
            evento_key = "desastre"
        else:
            evento_key = "emboscada"

    evento_key = aplicar_implantes_al_evento(evento_key, tipo_contrato, implantes)

    return EVENTOS[evento_key]
