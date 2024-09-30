def leer_archivo():
    with open("prueba.txt", "r") as archivo:
        lineas = archivo.readlines()
    
    # Leer dimensiones del tablero
    dimensiones = lineas[0].strip().split(',')
    filas = int(dimensiones[0])
    columnas = int(dimensiones[1])
    
    # Crear el tablero vacío
    tablero = []
    
    # Leer el resto de las líneas y llenar el tablero
    for linea in lineas[1:]:
        fila = [int(num) for num in linea.strip()]
        tablero.append(fila)
    
    return tablero
def imprimir_tablero(tablero):
    # Imprimir el tablero de forma legibl
    for fila in tablero:
        fila_imprimible = [' ' if num == 0 else str(num) for num in fila]
        print(" ".join(fila_imprimible))  # Unir los elementos con espacios


def menu_humano():
    print("Juego de Hashiwokakero")
    print("1. Crear Partida")
    opcion = input("Seleccione una opcion: ")
    if opcion == "1":
        print("CREAR PARTIDA")
        tablero = leer_archivo()
        imprimir_tablero(tablero)
    else:
        print("Opcion no valida")

def menu_juego():
    print("Juego de Hashiwokakero")
    print("1. Jugador Humano")
    print("2. Jugador Sintetico")
    print("3. Salir")
    opcion = input("Seleccione una opcion: ")
    if opcion == "1":
        print("MENU JUGADOR HUMANO")
        menu_humano()
    elif opcion == "2":
        print("MENU JUGADOR SINTETICO")
    elif opcion == "3":
        print("Saliendo del juego.")
    else:
        print("Opcion no valida")
        menu_juego()  # Volver a mostrar el menú en caso de opción no válida

def main():
    menu_juego()

if __name__ == "__main__":
    main()
