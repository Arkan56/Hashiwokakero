import numpy as np

def crear_matriz_adyacencia(num_islas, aristas):
    """Crea una matriz de adyacencia para representar las conexiones entre las islas."""
    matriz = np.zeros((num_islas, num_islas), dtype=int)
    return matriz

def leer_archivo():
    """Lee el archivo y devuelve el tablero, las islas y las aristas posibles."""
    with open("prueba.txt", "r") as archivo:
        lineas = archivo.readlines()
    
    dimensiones = lineas[0].strip().split(',')
    filas = int(dimensiones[0])
    columnas = int(dimensiones[1])
    
    tablero = []
    islas = {}
    isla_counter = 0

    for i, linea in enumerate(lineas[1:]):
        fila = [int(num) for num in linea.strip()]
        tablero.append(fila)
        
        for j, num in enumerate(fila):
            if num > 0:  # Solo si hay una isla
                islas[(i, j)] = isla_counter  # Guardar la posición y un ID único para la isla
                isla_counter += 1  # Incrementar el contador de islas
    
    aristas = generar_aristas(tablero, islas)
    return tablero, islas, aristas

def generar_aristas(tablero, islas):
    """Genera las posibles aristas (conexiones) entre las islas adyacentes."""
    aristas = []
    filas = len(tablero)
    columnas = len(tablero[0]) if filas > 0 else 0

    for (pos, isla_id) in islas.items():
        i, j = pos
        # Conectar horizontalmente
        for k in range(j + 1, columnas):
            if tablero[i][k] > 0:
                aristas.append((isla_id, islas[(i, k)]))  # Conectar las islas por ID
                break

        # Conectar verticalmente
        for k in range(i + 1, filas):
            if tablero[k][j] > 0:
                aristas.append((isla_id, islas[(k, j)]))  # Conectar las islas por ID
                break

    return aristas

def imprimir_tablero(tablero, islas):
    """Imprime el tablero con las islas y los puentes."""
    for i, fila in enumerate(tablero):
        fila_imprimible = []
        for j, celda in enumerate(fila):
            if (i, j) in islas:
                fila_imprimible.append(str(islas[(i, j)]))  # Mostrar ID de la isla
            elif celda == '-':
                fila_imprimible.append('-')  # Puente horizontal
            elif celda == '=':
                fila_imprimible.append('=')
            elif celda == '|':
                fila_imprimible.append('|')  # Puente vertical
            elif celda == '||':
                fila_imprimible.append('||')
            else:
                fila_imprimible.append(' ')  # Espacio vacío
        print(" ".join(fila_imprimible))

def mostrar_lista_islas(islas, tablero):
    """Imprime una lista de islas con sus posiciones y IDs."""
    print("\nLista de Islas:")
    print("ID\tPosición (fila, columna)\tPuentes Requeridos")
    for pos, id_isla in sorted(islas.items(), key=lambda x: x[1]):
        fila, columna = pos
        puentes = tablero[fila][columna]
        print(f"{id_isla}\t({fila}, {columna})\t\t\t{puentes}")
    print("\n")

def agregar_puente(tablero, matriz_adyacencia, isla_a, isla_b, islas):
    """Agrega un puente entre dos islas, si es válido, y actualiza el tablero visualmente."""
    if isla_a in islas.values() and isla_b in islas.values():  # Verificar si las islas existen
        if es_movimiento_valido(tablero, matriz_adyacencia, isla_a, isla_b, islas):
            matriz_adyacencia[isla_a][isla_b] += 1
            matriz_adyacencia[isla_b][isla_a] += 1

            # Obtener las posiciones de las islas por su ID
            pos_a = next(key for key, value in islas.items() if value == isla_a)
            pos_b = next(key for key, value in islas.items() if value == isla_b)
            i_a, j_a = pos_a
            i_b, j_b = pos_b

            # Dibujar el puente en el tablero
            if i_a == i_b:  # Movimiento horizontal
                paso = 1 if j_b > j_a else -1
                for j in range(j_a + paso, j_b, paso):
                    if matriz_adyacencia[isla_a][isla_b] == 1:
                        tablero[i_a][j] = '-'  # Un puente horizontal
                    elif matriz_adyacencia[isla_a][isla_b] == 2:
                        tablero[i_a][j] = '='  # Doble puente horizontal
            elif j_a == j_b:  # Movimiento vertical
                paso = 1 if i_b > i_a else -1
                for i in range(i_a + paso, i_b, paso):
                    if matriz_adyacencia[isla_a][isla_b] == 1:
                        tablero[i][j_a] = '|'  # Un puente vertical
                    elif matriz_adyacencia[isla_a][isla_b] == 2:
                        tablero[i][j_a] = '||'  # Doble puente vertical

            return True
        else:
            print(f"No se puede agregar el puente entre Isla {isla_a} e Isla {isla_b}.")
    else:
        print(f"Isla {isla_a} o Isla {isla_b} no encontrada.")
    return False

def es_movimiento_valido(tablero, matriz_adyacencia, isla_a, isla_b, islas):
    """Verifica si un movimiento es válido."""
    if isla_a not in islas.values() or isla_b not in islas.values():
        print("Una o ambas islas no son válidas.")
        return False

    # Obtener las posiciones de las islas por su ID
    pos_a = next(key for key, value in islas.items() if value == isla_a)
    pos_b = next(key for key, value in islas.items() if value == isla_b)

    i_a, j_a = pos_a
    i_b, j_b = pos_b

    # Verificar si las islas están en la misma fila o columna
    if i_a != i_b and j_a != j_b:
        print("Las islas no están alineadas.")
        return False

    # Verificar si hay obstáculos en el camino
    if i_a == i_b:  # Movimiento horizontal
        paso = 1 if j_b > j_a else -1
        for j in range(j_a + paso, j_b, paso):
            if tablero[i_a][j] > 0 and (i_a, j) not in islas:
                print("Hay una isla en el camino.")
                return False
            if tablero[i_a][j] in ['-', '=', '||', '|']:
                print("Hay un puente en el camino.")
                return False
    elif j_a == j_b:  # Movimiento vertical
        paso = 1 if i_b > i_a else -1
        for i in range(i_a + paso, i_b, paso):
            if tablero[i][j_a] > 0 and (i, j_a) not in islas:
                print("Hay una isla en el camino.")
                return False
            if tablero[i][j_a] in ['|', '||', '-', '=']:
                print("Hay un puente en el camino.")
                return False

    # Verificar si ya hay dos puentes entre las islas
    if matriz_adyacencia[isla_a][isla_b] >= 2:
        print("Ya hay dos puentes entre estas islas.")
        return False

    return True

def verificar_victoria(matriz_adyacencia, islas, tablero):
    """Verifica si todas las islas tienen el número correcto de puentes."""
    for (i, j), isla_id in islas.items():
        puentes = np.sum(matriz_adyacencia[isla_id])  # Total de puentes conectados a la isla
        if puentes != tablero[i][j]:
            return False  # La isla no tiene el número correcto de puentes
    return True

def imprimir_matriz_adyacencia(matriz_adyacencia):
    """Imprime la matriz de adyacencia."""
    print("\nMatriz de Adyacencia:")
    print(matriz_adyacencia)

def menu_humano():
    """Función para el modo de juego con jugador humano."""
    print("Juego de Hashiwokakero")
    print("1. Crear Partida")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        print("CREAR PARTIDA")
        tablero, islas, aristas = leer_archivo()
        matriz_adyacencia = crear_matriz_adyacencia(len(islas), aristas)

        # Mostrar la lista de islas y sus IDs
        mostrar_lista_islas(islas, tablero)
        
        while True:
            imprimir_tablero(tablero, islas)
            isla_a = int(input("Ingrese el ID de la primera isla a conectar: "))
            isla_b = int(input("Ingrese el ID de la segunda isla a conectar: "))

            if isla_a >= len(islas) or isla_b >= len(islas):
                print("Isla no válida.")
                continue

            if agregar_puente(tablero, matriz_adyacencia, isla_a, isla_b, islas):
                print(f"Puente agregado entre las islas {isla_a} y {isla_b}.")
            else:
                print("No se puede agregar el puente.")
            
            if verificar_victoria(matriz_adyacencia, islas, tablero):
                imprimir_tablero(tablero, islas)  # Mostrar el tablero final con todos los puentes
                print("¡Felicidades! Todas las islas están conectadas correctamente.")
                break
            else:
                print("Aún faltan conexiones correctas.")
    else:
        print("Opción no válida")

def menu_juego():
    """Menú principal del juego."""
    print("Juego de Hashiwokakero")
    print("1. Jugador Humano")
    print("2. Jugador Sintético")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        print("MENU JUGADOR HUMANO")
        menu_humano()
    elif opcion == "2":
        print("MENU JUGADOR SINTÉTICO")
        # Aquí puedes implementar un jugador automático en el futuro
    elif opcion == "3":
        print("Saliendo del juego.")
    else:
        print("Opción no válida")
        menu_juego()

def main():
    """Función principal del juego."""
    menu_juego()

if __name__ == "__main__":
    main()
