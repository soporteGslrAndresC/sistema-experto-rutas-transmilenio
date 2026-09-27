# base_conocimiento.py

ESTACIONES = {
    "portal_norte":     {"nombre": "Portal Norte",        "x": 4.0,  "y": 20.0},
    "toberin":          {"nombre": "Toberín",             "x": 4.0,  "y": 18.5},
    "mazuren":          {"nombre": "Mazurén",             "x": 4.0,  "y": 17.0},
    "alcala":           {"nombre": "Alcalá",              "x": 5.0,  "y": 18.0},
    "prado":            {"nombre": "Prado",               "x": 5.0,  "y": 16.5},
    "calle_100":        {"nombre": "Calle 100",           "x": 4.2,  "y": 15.0},
    "calle_85":         {"nombre": "Calle 85",            "x": 4.2,  "y": 13.5},
    "heroes":           {"nombre": "Héroes",              "x": 4.2,  "y": 12.0},
    "calle_76":         {"nombre": "Calle 76",            "x": 4.2,  "y": 11.0},
    "chapinero":        {"nombre": "Chapinero",           "x": 4.2,  "y": 9.8},
    "calle_45":         {"nombre": "Calle 45",            "x": 4.0,  "y": 8.5},
    "av_jimenez":       {"nombre": "Av. Jiménez",         "x": 3.8,  "y": 6.8},
    "tercer_milenio":   {"nombre": "Tercer Milenio",      "x": 3.7,  "y": 5.6},
    "hospitales":       {"nombre": "Hospitales",          "x": 3.6,  "y": 4.4},
    "restrepo":         {"nombre": "Restrepo",            "x": 3.4,  "y": 2.9},
    "portal_sur":       {"nombre": "Portal Sur",          "x": 3.2,  "y": 0.5},
    "polo":             {"nombre": "Polo",                "x": 1.5,  "y": 12.0},
    "ricaurte":         {"nombre": "Ricaurte",            "x": 1.8,  "y": 7.0},
    "cad":              {"nombre": "CAD",                 "x": 2.0,  "y": 8.2},
    "comuneros":        {"nombre": "Comuneros",           "x": 2.5,  "y": 3.0},
}


CONEXIONES = [
    # Troncal Caracas (norte - sur)
    ("portal_norte", "toberin", "caracas", 3),
    ("toberin", "mazuren", "caracas", 2),
    ("mazuren", "calle_100", "caracas", 3),
    ("calle_100", "calle_85", "caracas", 3),
    ("calle_85", "heroes", "caracas", 3),
    ("heroes", "calle_76", "caracas", 2),
    ("calle_76", "chapinero", "caracas", 2),
    ("chapinero", "calle_45", "caracas", 3),
    ("calle_45", "av_jimenez", "caracas", 4),
    ("av_jimenez", "tercer_milenio", "caracas", 2),
    ("tercer_milenio", "hospitales", "caracas", 3),
    ("hospitales", "restrepo", "caracas", 4),
    ("restrepo", "portal_sur", "caracas", 5),

    # Troncal Autonorte (se junta con Caracas en Calle 100 y en Héroes)
    ("portal_norte", "alcala", "autonorte", 3),
    ("alcala", "prado", "autonorte", 3),
    ("prado", "calle_100", "autonorte", 3),
    ("calle_100", "heroes", "autonorte", 5),

    # Troncal NQS (occidente, cruza con Caracas en varios puntos)
    ("portal_sur", "comuneros", "nqs", 4),
    ("comuneros", "ricaurte", "nqs", 5),
    ("ricaurte", "cad", "nqs", 3),
    ("cad", "polo", "nqs", 6),
    ("polo", "heroes", "nqs", 4),
    ("ricaurte", "av_jimenez", "nqs", 3),   # conexión peatonal corta entre troncales
]


PENALIZACION_TRANSBORDO = 4  # minutos


def costo_transbordo(linea_actual, linea_siguiente):
    """
    Regla lógica:
        SI linea_actual != linea_siguiente  ENTONCES  costo = PENALIZACION_TRANSBORDO
        SI NO                                ENTONCES  costo = 0
    """
    if linea_actual is None:
        # todavía no se ha tomado ningún bus, así que no hay transbordo
        return 0
    if linea_actual != linea_siguiente:
        return PENALIZACION_TRANSBORDO
    return 0


def construir_grafo():
    """
    A partir de los hechos (CONEXIONES) arma un diccionario de
    adyacencia. Cada estación queda apuntando a la lista de estaciones
    vecinas con las que tiene conexión directa, indicando la línea y
    el tiempo de viaje.

    grafo["heroes"] -> [("calle_76", "caracas", 2), ("calle_85", "caracas", 3), ...]
    """
    grafo = {estacion: [] for estacion in ESTACIONES}

    for origen, destino, linea, tiempo in CONEXIONES:
        grafo[origen].append((destino, linea, tiempo))
        grafo[destino].append((origen, linea, tiempo))  # no dirigido

    return grafo


def existe_estacion(nombre_clave):
    return nombre_clave in ESTACIONES


def nombre_bonito(clave):
    return ESTACIONES[clave]["nombre"]
