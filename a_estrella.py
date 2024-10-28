import heapq
from nodo import Nodo
from casilla import Casilla


# Heurística de Manhattan
def manhattan_heuristica(nodo_actual, nodo_meta):
    """Calcula la distancia Manhattan entre dos nodos (usando Casilla)."""
    resultado = abs(nodo_actual.getFila() - nodo_meta.getFila()) + abs(nodo_actual.agetCol() - nodo_meta.getCol())
    return resultado

# Heurística trivial (siempre devuelve 0)
def trivial_heuristica(nodo_actual, nodo_meta):
    return 0

# Heurística euclídea (distancia directa en línea recta)
def euclidea_heuristica(nodo_actual, nodo_meta):
    return ((nodo_actual.getFila() - nodo_meta.getFila())**2 + (nodo_actual.getCol() - nodo_meta.getCol())**2)**0.5

# Heurística de Chebyshev (considera movimientos diagonales)
def chebyshev_heuristica(nodo_actual, nodo_meta):
    return max(abs(nodo_actual.getFila() - nodo_meta.getFila()), abs(nodo_actual.getCol() - nodo_meta.getCol()))


def a_estrella(camino, inicio, meta, obtener_vecinos, costo_movimiento, tipo_heuristica):
    """Algoritmo A* que encuentra el camino óptimo entre 'inicio' y 'meta'."""
    lista_frontera = []
    lista_interior = set()

    # Nodo inicial con la heurística seleccionada
    nodo_inicial = Nodo(inicio, None, 0, tipo_heuristica(inicio, meta))
    heapq.heappush(lista_frontera, nodo_inicial)
    
    cal = 0  # Calorías (puedes ajustar este valor según la lógica)
    f_final = -1  # Coste final, inicialmente -1

    while lista_frontera:
        nodo_actual = heapq.heappop(lista_frontera)

        # Si el nodo actual ya ha sido expandido, lo ignoramos
        if nodo_actual.getEstado() in lista_interior:
            continue

        # Añadir el nodo actual a la lista interior (nodos ya explorados)
        lista_interior.add(nodo_actual.getEstado())

        # Si hemos llegado al nodo destino, reconstruir el camino
        if nodo_actual.getEstado().getFila() == meta.getFila() and nodo_actual.getEstado().getCol() == meta.getCol():
            # Reconstruir el camino desde el nodo final al inicial
            camino_reconstruido = reconstruir_camino(nodo_actual)
            
            # Marcar el camino en el mapa cambiando '.' por '*'
            for casilla in camino_reconstruido:
                fila = casilla.getFila()
                columna = casilla.getCol()
                camino[fila][columna] = '*'  # Marcar el camino en el mapa
            
            f_final = nodo_actual.f  # El coste final es el valor de 'f' del nodo meta
            return f_final, cal  # Devolver el coste final y las calorías

        # Expandir los vecinos del nodo actual
        for vecino in obtener_vecinos(nodo_actual.getEstado()):
            if vecino in lista_interior:
                continue  # Saltar los nodos que ya fueron expandidos
            
            # Calcular nuevo g (coste desde el inicio)
            g_nuevo = nodo_actual.g + costo_movimiento(nodo_actual.getEstado(), vecino)
            
            # Crear un nodo vecino con la heurística seleccionada
            nodo_vecino = Nodo(vecino, nodo_actual, g_nuevo, tipo_heuristica(vecino, meta))

            # Añadir el nodo vecino a la lista frontera si no está ya
            if nodo_vecino not in lista_frontera:
                heapq.heappush(lista_frontera, nodo_vecino)

    # Si no se encuentra un camino válido
    return -1, cal  # Devuelve -1 para el coste si no se encuentra un camino válido


def reconstruir_camino(nodo):
    """Reconstruir el camino desde el nodo final hasta el inicial."""
    camino = []
    while nodo is not None:
        camino.append(nodo.getEstado())  # Agregar el estado del nodo actual
        nodo = nodo.padre
    return camino[::-1]  # Invertir el camino para que vaya desde el inicio al final
