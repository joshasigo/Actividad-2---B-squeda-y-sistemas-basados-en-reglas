1. introducción

El presente readme describe el desarrollo de un sistema inteligente basado en conocimiento capaz de determinar la ruta optima entre dos estaciones del sistema de transporte masivo TransMilenio en Bogotá, Colombia. El sistema fue implementado en lenguaje Python 3 y utiliza el algoritmo de búsqueda heurística A* (A estrella), combinado con una base de conocimiento representada mediante reglas lógicas del tipo hechos y conexiones.
Este trabajo corresponde a la Actividad 2 del curso de Inteligencia Artificial, y se enmarca en los conceptos desarrollados en los capítulos 2 (lógica y representación del conocimiento), 3 (Sistemas basados en reglas) y 9 (técnicas basadas en búsquedas heurísticas) del libro de referencia: Benitez, R. (2014). Inteligencia artificial avanzada. Editorial UOC.

2. descripción del Sistema

El sistema actúa como un agente inteligente que recibe como entrada el nombre de una estación de origen y una estación de destino, y produce como salida la ruta optima expresada como una secuencia de estaciones, incluyendo el tiempo estimado de viaje y las líneas utilizadas. Internamente, el sistema combina tres componentes principales:
•	Base de conocimiento: conjunto de hechos y reglas lógicas sobre la red de TransMilenio.
•	Motor de inferencia: el algoritmo A* que aplica las reglas para encontrar la solución óptima.
•	Heuristica: la función de distancia Haversine convertida a minutos, que guía la búsqueda.

2.1 Estructura del código
El Código fuente está organizado en los siguientes módulos funcionales:

1.	Bloque de constantes: ESTACIONES (coordenadas) y REGLAS_CONEXION (hechos lógicos).
2.	Funcion construir_grafo(): convierte las reglas en un grafo bidireccional.
3.	Funcion heuristica_haversine(): calcula h(n) con coordenadas geograficas reales.
4.	Funcion algoritmo_a_estrella(): implementa el algoritmo A* con cola de prioridad.
5.	Funciones de presentacion e interfaz: mostrar_ruta(), menu_interactivo(), ejecutar_pruebas().
