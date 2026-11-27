import os
from config import ARCHIVO_BUSES, ARCHIVO_CIUDADES, ARCHIVO_CLIENTES
from config import ARCHIVO_PASAJES, ARCHIVO_VIAJES, ENCODE


# Lee un csv y devuelve una lista de filas (cada fila es una lista de textos)
def leer_filas(ruta):
    filas = []
    if not os.path.exists(ruta):
        return filas
    f = open(ruta, "r", encoding=ENCODE)
    lineas = f.readlines()
    f.close()
    for linea in lineas:
        if linea.strip() != "":
            fila = []
            for dato in linea.strip().split(","):
                fila.append(dato.strip())
            filas.append(fila)
    return filas


# ciudad: [id, nombre, posicion]
def cargar_ciudades():
    ciudades = []
    for fila in leer_filas(ARCHIVO_CIUDADES)[1:]:
        if len(fila) >= 3:
            ciudades.append([fila[0], fila[1], int(fila[2])])
    if len(ciudades) == 0:
        ciudades = [["CIU_01", "Concepción", 0], ["CIU_02", "Chillán", 1],
                    ["CIU_03", "Linares", 2], ["CIU_04", "Talca", 3],
                    ["CIU_05", "Rancagua", 4], ["CIU_06", "Santiago", 5]]
    return ciudades


# bus: [id_bus, patente, capacidad, estado]
def cargar_buses():
    buses = []
    for fila in leer_filas(ARCHIVO_BUSES)[1:]:
        if len(fila) >= 4:
            buses.append([fila[0], fila[1], int(fila[2]), fila[3]])
    return buses


# cliente: [id, rut, nombres, ap_paterno, ap_materno, contacto]
def cargar_clientes():
    clientes = []
    for fila in leer_filas(ARCHIVO_CLIENTES)[1:]:
        if len(fila) >= 6:
            clientes.append(fila[:6])
    return clientes


# viaje: [id_viaje, id_bus, fecha, hora, origen, destino, tarifa_base]
def cargar_viajes():
    viajes = []
    for fila in leer_filas(ARCHIVO_VIAJES):
        if fila[0].lower() == "id_viaje":
            continue
        if len(fila) >= 7:
            viajes.append([fila[0], fila[1], fila[2], fila[3],
                           fila[4], fila[5], int(fila[6])])
    return viajes


# pasaje: [id_pasaje, id_viaje, id_cliente, origen, destino, asiento, valor, estado]
def cargar_pasajes():
    pasajes = []
    for fila in leer_filas(ARCHIVO_PASAJES):
        if fila[0].lower() == "id_pasaje":
            continue
        if len(fila) >= 8:
            pasajes.append([fila[0], fila[1], fila[2], fila[3], fila[4],
                            int(fila[5]), int(fila[6]), fila[7]])
    return pasajes
