from base_conocimiento import ESTACIONES, existe_estacion
from busqueda import imprimir_ruta


def mostrar_estaciones_disponibles():
    print("\nEstaciones disponibles:")
    for clave, datos in ESTACIONES.items():
        print(f"  {clave:15s} -> {datos['nombre']}")


def pedir_estacion(mensaje):
    while True:
        clave = input(mensaje).strip().lower().replace(" ", "_")
        if existe_estacion(clave):
            return clave
        print("Esa estación no existe en la base de conocimiento. Revisa el listado.")


def modo_interactivo():
    print("=" * 55)
    print(" SISTEMA EXPERTO DE RUTAS - TRANSPORTE MASIVO (demo)")
    print("=" * 55)
    mostrar_estaciones_disponibles()

    origen = pedir_estacion("\nEscribe la estación de ORIGEN: ")
    destino = pedir_estacion("Escribe la estación de DESTINO: ")

    imprimir_ruta(origen, destino)


def modo_pruebas():
    """
    Corre unos casos de prueba fijos, útil para el video y para el PDF
    de pruebas que hay que entregar.
    """
    casos = [
        ("portal_norte", "portal_sur"),
        ("toberin", "restrepo"),
        ("polo", "portal_norte"),
        ("comuneros", "calle_85"),
        ("portal_norte", "portal_norte"),  # caso trivial, origen = destino
    ]

    for origen, destino in casos:
        imprimir_ruta(origen, destino)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--pruebas":
        modo_pruebas()
    else:
        modo_interactivo()
