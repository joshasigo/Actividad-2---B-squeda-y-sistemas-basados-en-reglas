"""
=============================================================
  SISTEMA INTELIGENTE DE RUTAS - TRANSMILENIO BOGOTÁ
  Algoritmo de Búsqueda Heurística A* (A estrella)
  Base de Conocimiento representada en Reglas Lógicas
=============================================================

Curso: Inteligencia Artificial
Actividad 3 - Sistemas Basados en Conocimiento y Búsqueda Heurística

Referencia:
  Benítez, R. (2014). Inteligencia artificial avanzada. Barcelona: Editorial UOC.
  - Capítulo 2: Lógica y representación del conocimiento
  - Capítulo 3: Sistemas basados en reglas
  - Capítulo 9: Técnicas basadas en búsquedas heurísticas
"""

import heapq
import math


# =============================================================
# BASE DE CONOCIMIENTO: REGLAS LÓGICAS
# Representación: hechos y reglas sobre la red de TransMilenio
# =============================================================

# HECHOS: Estaciones y sus coordenadas geográficas aproximadas
# Formato: "Nombre": (latitud, longitud)
ESTACIONES = {
    # Troncal Caracas (Norte-Sur)
    "Portal Norte":         (4.7602, -74.0457),
    "Toberin":              (4.7440, -74.0480),
    "Cardio Infantil":      (4.7280, -74.0500),
    "Mazuren":              (4.7170, -74.0510),
    "Alcalá":               (4.7080, -74.0520),
    "Pepe Sierra":          (4.6990, -74.0530),
    "Calle 100":            (4.6880, -74.0540),
    "Calle 72":             (4.6670, -74.0520),
    "Calle 63":             (4.6570, -74.0510),
    "Flores":               (4.6480, -74.0500),
    "Calle 45":             (4.6380, -74.0490),
    "Marly":                (4.6290, -74.0480),
    "Calle 26":             (4.6180, -74.0840),
    "Ricaurte":             (4.6100, -74.0960),
    "Calle 8":              (4.6010, -74.0960),
    "General Santander":    (4.5920, -74.0960),
    "Sevillana":            (4.5830, -74.0960),
    "Portal Sur":           (4.5680, -74.0970),

    # Troncal NQS (Norte-Sur alternativa)
    "Portal 80":            (4.6930, -74.1140),
    "Avenida Rojas":        (4.6820, -74.1130),
    "Gratamira":            (4.6720, -74.1120),
    "Niza Calle 127":       (4.7060, -74.0700),
    "Calle 76":             (4.6690, -74.0700),
    "Escuela Militar":      (4.6570, -74.0490),

    # Troncal Américas (Occidente)
    "Portal Américas":      (4.6280, -74.1770),
    "Banderas":             (4.6320, -74.1600),
    "Patio Bonito":         (4.6360, -74.1440),
    "Tintal":               (4.6390, -74.1310),
    "Alquería":             (4.6290, -74.1070),
    "Marsella":             (4.6290, -74.1020),

    # Estaciones clave centro
    "Museo del Oro":        (4.6010, -74.0720),
    "Las Aguas":            (4.6040, -74.0670),
    "Universidades":        (4.6100, -74.0800),
    "El Tiempo Maloka":     (4.6570, -74.1130),
    "El Dorado":            (4.6620, -74.1070),
    "Av. Eldorado":         (4.6580, -74.1000),

    # Portal Usme (Sur)
    "Portal Usme":          (4.5140, -74.1090),
    "Molinos":              (4.5370, -74.1020),
    "Biblioteca":           (4.5540, -74.0990),
    "Parque El Tunal":      (4.5640, -74.1000),
    "Venecia":              (4.5750, -74.1000),
}


# REGLAS LÓGICAS: Conexiones entre estaciones
# Formato: (estacion_origen, estacion_destino, tiempo_minutos, linea)
# Regla: SI estacion_A conecta_con estacion_B ENTONCES se puede viajar entre ellas
REGLAS_CONEXION = [
    # --- Troncal Caracas Norte-Sur ---
    ("Portal Norte",        "Toberin",           5,  "B11"),
    ("Toberin",             "Cardio Infantil",   4,  "B11"),
    ("Cardio Infantil",     "Mazuren",           3,  "B11"),
    ("Mazuren",             "Alcalá",            3,  "B11"),
    ("Alcalá",              "Pepe Sierra",       3,  "B11"),
    ("Pepe Sierra",         "Calle 100",         4,  "B11"),
    ("Calle 100",           "Calle 72",          5,  "B11"),
    ("Calle 72",            "Calle 63",          4,  "B11"),
    ("Calle 63",            "Flores",            3,  "B11"),
    ("Flores",              "Calle 45",          4,  "B11"),
    ("Calle 45",            "Marly",             3,  "B11"),
    ("Marly",               "Calle 26",          5,  "B11"),
    ("Calle 26",            "Ricaurte",          4,  "C12"),
    ("Ricaurte",            "Calle 8",           3,  "C12"),
    ("Calle 8",             "General Santander", 4,  "C12"),
    ("General Santander",   "Sevillana",         3,  "C12"),
    ("Sevillana",           "Portal Sur",        4,  "C12"),

    # --- Troncal NQS ---
    ("Portal 80",           "Avenida Rojas",     5,  "H19"),
    ("Avenida Rojas",       "Gratamira",         4,  "H19"),
    ("Gratamira",           "El Tiempo Maloka",  5,  "H19"),
    ("El Tiempo Maloka",    "El Dorado",         3,  "H19"),
    ("El Dorado",           "Av. Eldorado",      3,  "H19"),
    ("Av. Eldorado",        "Calle 26",          4,  "H19"),

    # --- Troncal Américas ---
    ("Portal Américas",     "Banderas",          5,  "G14"),
    ("Banderas",            "Patio Bonito",      4,  "G14"),
    ("Patio Bonito",        "Tintal",            4,  "G14"),
    ("Tintal",              "Alquería",          5,  "G14"),
    ("Alquería",            "Marsella",          3,  "G14"),
    ("Marsella",            "Ricaurte",          5,  "G14"),

    # --- Conexiones transversales (trasbordos) ---
    ("Calle 26",            "Museo del Oro",     6,  "TRANSV"),
    ("Museo del Oro",       "Las Aguas",         4,  "TRANSV"),
    ("Las Aguas",           "Universidades",     3,  "TRANSV"),
    ("Calle 26",            "El Dorado",         7,  "TRANSV"),
    ("Calle 100",           "Niza Calle 127",    5,  "TRANSV"),
    ("Calle 72",            "Calle 76",          4,  "TRANSV"),
    ("Calle 63",            "Escuela Militar",   3,  "TRANSV"),

    # --- Troncal Sur ---
    ("Portal Usme",         "Molinos",           5,  "P14"),
    ("Molinos",             "Biblioteca",        4,  "P14"),
    ("Biblioteca",          "Parque El Tunal",   4,  "P14"),
    ("Parque El Tunal",     "Venecia",           3,  "P14"),
    ("Venecia",             "General Santander", 4,  "P14"),
]


# =============================================================
# CONSTRUCCIÓN DEL GRAFO A PARTIR DE LAS REGLAS
# =============================================================

def construir_grafo(reglas):
    """
    Convierte las reglas lógicas de conexión en un grafo bidireccional.
    Regla: conexion(A, B, T, L) => grafo[A][B] = (T, L) y grafo[B][A] = (T, L)
    """
    grafo = {est: {} for est in ESTACIONES}
    for origen, destino, tiempo, linea in reglas:
        if origen in grafo and destino in grafo:
            grafo[origen][destino] = (tiempo, linea)
            grafo[destino][origen] = (tiempo, linea)
    return grafo


# =============================================================
# HEURÍSTICA: Distancia Haversine (distancia geográfica real)
# Usada por A* para estimar el costo restante hasta el destino
# =============================================================

def heuristica_haversine(est_actual, est_destino):
    """
    Calcula la distancia en km entre dos estaciones usando la fórmula de Haversine.
    Se asume una velocidad promedio de 30 km/h para convertir a minutos.
    """
    lat1, lon1 = ESTACIONES[est_actual]
    lat2, lon2 = ESTACIONES[est_destino]

    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia_km = R * c

    # Convertir a minutos asumiendo 30 km/h promedio
    tiempo_estimado = (distancia_km / 30) * 60
    return tiempo_estimado


# =============================================================
# ALGORITMO A* - BÚSQUEDA HEURÍSTICA
# =============================================================

def algoritmo_a_estrella(grafo, inicio, destino):
    """
    Implementación del algoritmo A* para encontrar la ruta óptima.

    Estructura de la cola de prioridad:
      (f(n), g(n), nodo_actual, camino_recorrido, lineas_usadas)
    donde:
      f(n) = g(n) + h(n)
      g(n) = costo real acumulado (minutos)
      h(n) = heurística (estimación de minutos restantes)

    Returns:
      (ruta, tiempo_total, lineas) o None si no hay ruta
    """
    if inicio not in grafo:
        return None, None, None
    if destino not in grafo:
        return None, None, None
    if inicio == destino:
        return [inicio], 0, []

    h_inicial = heuristica_haversine(inicio, destino)
    # Cola: (f, g, nodo, ruta, lineas_usadas)
    cola = [(h_inicial, 0, inicio, [inicio], [])]
    visitados = {}

    while cola:
        f, g, nodo_actual, ruta, lineas = heapq.heappop(cola)

        if nodo_actual in visitados and visitados[nodo_actual] <= g:
            continue
        visitados[nodo_actual] = g

        if nodo_actual == destino:
            return ruta, g, lineas

        for vecino, (tiempo, linea) in grafo[nodo_actual].items():
            nuevo_g = g + tiempo
            if vecino in visitados and visitados[vecino] <= nuevo_g:
                continue
            h = heuristica_haversine(vecino, destino)
            nuevo_f = nuevo_g + h
            nueva_ruta = ruta + [vecino]
            nuevas_lineas = lineas + [(nodo_actual, vecino, linea, tiempo)]
            heapq.heappush(cola, (nuevo_f, nuevo_g, vecino, nueva_ruta, nuevas_lineas))

    return None, None, None  # No se encontró ruta


# =============================================================
# PRESENTACIÓN DE RESULTADOS
# =============================================================

def mostrar_ruta(ruta, tiempo_total, lineas, inicio, destino):
    """Muestra la ruta encontrada de forma clara y detallada."""
    separador = "=" * 60

    print(f"\n{separador}")
    print("  🚌 SISTEMA DE RUTAS TRANSMILENIO - BOGOTÁ")
    print("     Algoritmo A* (A estrella)")
    print(separador)

    if ruta is None:
        print(f"\n  ❌ No se encontró ruta entre '{inicio}' y '{destino}'.")
        print(f"  Verifica que las estaciones existan en la red.\n")
        return

    print(f"\n  📍 Origen:  {inicio}")
    print(f"  🏁 Destino: {destino}")
    print(f"  ⏱️  Tiempo estimado: {tiempo_total:.1f} minutos")
    print(f"  🔢 Número de paradas: {len(ruta) - 1}")
    print()
    print("  📋 DETALLE DE LA RUTA:")
    print("  " + "-" * 56)

    linea_actual = None
    for i, (origen_seg, destino_seg, linea, tiempo) in enumerate(lineas):
        if linea != linea_actual:
            print(f"\n  🚌 Línea: {linea}")
            linea_actual = linea
            if i > 0:
                print(f"     ↕️  [TRANSBORDO en {origen_seg}]")
        print(f"     {i+1:2}. {origen_seg} → {destino_seg}  ({tiempo} min)")

    print(f"\n  🏁 Llegada a: {destino}")
    print(f"\n{separador}")
    print(f"  ✅ Ruta encontrada con {len(ruta)} estaciones.")
    print(separador)


def listar_estaciones():
    """Lista todas las estaciones disponibles."""
    print("\n" + "=" * 60)
    print("  📋 ESTACIONES DISPONIBLES EN LA RED")
    print("=" * 60)
    for i, est in enumerate(sorted(ESTACIONES.keys()), 1):
        print(f"  {i:2}. {est}")
    print("=" * 60)


# =============================================================
# MENÚ INTERACTIVO
# =============================================================

def menu_interactivo(grafo):
    """Interfaz de texto para que el usuario ingrese origen y destino."""
    while True:
        print("\n" + "=" * 60)
        print("  🚌 TRANSMILENIO - BUSCADOR DE RUTAS CON A*")
        print("=" * 60)
        print("  1. Buscar ruta")
        print("  2. Ver estaciones disponibles")
        print("  3. Salir")
        print("=" * 60)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            listar_estaciones()
            print()
            inicio = input("  Ingrese la estación de ORIGEN: ").strip()
            destino = input("  Ingrese la estación de DESTINO: ").strip()

            ruta, tiempo, lineas = algoritmo_a_estrella(grafo, inicio, destino)
            mostrar_ruta(ruta, tiempo, lineas, inicio, destino)

        elif opcion == "2":
            listar_estaciones()

        elif opcion == "3":
            print("\n  ¡Hasta pronto! 🚌\n")
            break
        else:
            print("  ⚠️  Opción no válida.")


# =============================================================
# PRUEBAS AUTOMÁTICAS
# =============================================================

def ejecutar_pruebas(grafo):
    """Ejecuta un conjunto de casos de prueba predefinidos."""
    casos_prueba = [
        ("Portal Norte", "Portal Sur",      "Ruta completa Norte-Sur"),
        ("Portal Américas", "Portal Norte",  "Ruta Occidente a Norte"),
        ("Portal Usme", "Portal 80",         "Ruta Sur a Occidente"),
        ("Museo del Oro", "Calle 100",       "Ruta centro a norte"),
        ("Portal Norte", "Portal Norte",     "Mismo origen y destino"),
        ("Calle 72", "Venecia",              "Ruta media distancia"),
    ]

    print("\n" + "=" * 60)
    print("  🧪 EJECUCIÓN DE PRUEBAS AUTOMÁTICAS")
    print("=" * 60)

    for inicio, destino, descripcion in casos_prueba:
        print(f"\n  📌 Prueba: {descripcion}")
        ruta, tiempo, lineas = algoritmo_a_estrella(grafo, inicio, destino)
        mostrar_ruta(ruta, tiempo, lineas, inicio, destino)
        input("\n  Presione ENTER para la siguiente prueba...")


# =============================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================

if __name__ == "__main__":
    print("\n  Construyendo base de conocimiento y grafo de la red...")
    grafo = construir_grafo(REGLAS_CONEXION)
    print(f"  ✅ Red cargada: {len(ESTACIONES)} estaciones, "
          f"{len(REGLAS_CONEXION)} conexiones.\n")

    print("  ¿Cómo desea ejecutar el sistema?")
    print("  1. Modo interactivo")
    print("  2. Ejecutar pruebas automáticas")
    modo = input("  Seleccione (1/2): ").strip()

    if modo == "2":
        ejecutar_pruebas(grafo)
    else:
        menu_interactivo(grafo)
