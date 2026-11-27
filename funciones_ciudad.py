from algoritmos import busqueda_secuencial
from persistencia import cargar_ciudades


# Busca una ciudad por su id, por su nombre o por su posicion
def obtener_ciudad(ciudades, valor):
    ciudad = busqueda_secuencial(ciudades, 0, valor)
    if ciudad is None:
        ciudad = busqueda_secuencial(ciudades, 1, valor)
    if ciudad is None:
        ciudad = busqueda_secuencial(ciudades, 2, valor)
    return ciudad


def listar_ciudades():
    ciudades = cargar_ciudades()
    print(f"{'POSICIÓN':<10} {'ID':<10} CIUDAD")
    for c in ciudades:
        print(f"{c[2]:<10} {c[0]:<10} {c[1]}")
