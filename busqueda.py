

import heapq
import math

from base_conocimiento import (
    ESTACIONES,
    construir_grafo,
    costo_transbordo,
    nombre_bonito,
)

VELOCIDAD_PROMEDIO_KM_MIN = 0.5  # km que recorre el sistema por minuto (aprox)


def heuristica(estacion_actual, estacion_destino):
    """
    Distancia euclidiana entre dos estaciones, convertida a minutos
    estimados según la velocidad promedio del sistema.
    """
    x1, y1 = ESTACIONES[estacion_actual]["x"], ESTACIONES[estacion_actual]["y"]
    x2, y2 = ESTACIONES[estacion_destino]["x"], ESTACIONES[estacion_destino]["y"]

    distancia = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distancia / VELOCIDAD_PROMEDIO_KM_MIN


def buscar_ruta(origen, destino):
    """
    Búsqueda A* sobre el grafo del sistema de transporte.

    Un detalle importante: el "estado" de cada nodo en la búsqueda no es
    solo la estación, sino el par (estacion, linea_con_la_que_se_llego).
    Esto es necesario porque el costo de moverse depende de si hay que
    hacer transbordo o no, y eso solo se sabe si se conoce con qué línea
    se llegó a la estación actual.

    Retorna una tupla (ruta, costo_total, numero_de_transbordos) o
    (None, None, None) si no existe camino.
    """
    grafo = construir_grafo()

    # cola de prioridad: (f, g, estacion, linea_actual)
    # f = g + h  (costo recorrido + estimado hasta el destino)
    frontera = []
    estado_inicial = (origen, None)
    heapq.heappush(frontera, (heuristica(origen, destino), 0, origen, None))

    costos_conocidos = {estado_inicial: 0}
    padres = {estado_inicial: None}

    visitados = set()

    while frontera:
        f_actual, g_actual, estacion_actual, linea_actual = heapq.heappop(frontera)
        estado_actual = (estacion_actual, linea_actual)

        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)

        if estacion_actual == destino:
            return _reconstruir_ruta(padres, estado_actual, g_actual)

        for vecino, linea_vecino, tiempo_viaje in grafo[estacion_actual]:
            extra_transbordo = costo_transbordo(linea_actual, linea_vecino)
            costo_arco = tiempo_viaje + extra_transbordo

            nuevo_g = g_actual + costo_arco
            nuevo_estado = (vecino, linea_vecino)

            if nuevo_estado not in costos_conocidos or nuevo_g < costos_conocidos[nuevo_estado]:
                costos_conocidos[nuevo_estado] = nuevo_g
                padres[nuevo_estado] = estado_actual
                nueva_f = nuevo_g + heuristica(vecino, destino)
                heapq.heappush(frontera, (nueva_f, nuevo_g, vecino, linea_vecino))

    # si se vacía la frontera sin llegar al destino, no hay ruta posible
    return None, None, None


def _reconstruir_ruta(padres, estado_final, costo_total):
    """
    Sigue los punteros "padre" desde el estado final hasta el inicial
    para armar la ruta en orden correcto (origen -> destino), y de paso
    cuenta cuántos transbordos hubo en el camino.
    """
    camino = []
    estado = estado_final
    while estado is not None:
        camino.append(estado)
        estado = padres[estado]
    camino.reverse()

    # contar transbordos: cada vez que la línea cambia de un paso a otro
    transbordos = 0
    linea_previa = None
    for _, linea in camino:
        if linea_previa is not None and linea is not None and linea != linea_previa:
            transbordos += 1
        if linea is not None:
            linea_previa = linea

    return camino, costo_total, transbordos


def imprimir_ruta(origen, destino):
    """
    Función de conveniencia para mostrar el resultado de forma legible
    en consola, incluyendo cambios de línea.
    """
    camino, costo_total, transbordos = buscar_ruta(origen, destino)

    if camino is None:
        print(f"No se encontró una ruta entre {nombre_bonito(origen)} y {nombre_bonito(destino)}.")
        return

    print(f"\nRuta desde {nombre_bonito(origen)} hasta {nombre_bonito(destino)}:")
    print("-" * 50)

    linea_anterior = None
    for estacion, linea in camino:
        if linea is None:
            print(f"  Salida: {nombre_bonito(estacion)}")
        else:
            if linea != linea_anterior:
                print(f"  >> Tomar troncal '{linea}'")
            print(f"     - {nombre_bonito(estacion)}")
        linea_anterior = linea if linea is not None else linea_anterior

    print("-" * 50)
    print(f"Tiempo total estimado: {costo_total} min")
    print(f"Número de transbordos: {transbordos}")
