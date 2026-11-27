from datetime import datetime
from config import ARCHIVO_VIAJES, ENCODE
from algoritmos import busqueda_secuencial
from persistencia import cargar_viajes, cargar_buses, cargar_ciudades
from funciones_ciudad import obtener_ciudad


def registrar_viaje(id_bus, fecha, hora, origen, destino, tarifa):
    bus = busqueda_secuencial(cargar_buses(), 0, id_bus)
    if bus is None:
        print("El bus no existe")
        return False
    if bus[3].upper() == "NO DISPONIBLE":
        print("El bus no está disponible.")
        return False

    if not ((origen == 0 and destino == 5) or (origen == 5 and destino == 0)):
        print("Solo se programan viajes Concepción-Santiago o Santiago-Concepción")
        return False

    if len(fecha) != 10 or len(hora) != 5 or tarifa <= 0:
        print("Fecha, hora o tarifa inválidas")
        return False
    try:
        datetime.strptime(fecha + " " + hora, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Fecha u hora inválida.")
        return False

    viajes = cargar_viajes()
    for v in viajes:
        if v[1].upper() == id_bus.upper() and v[2] == fecha and v[3] == hora:
            print("El bus ya tiene un viaje a esa fecha y hora")
            return False

    f = open(ARCHIVO_VIAJES, "a", encoding=ENCODE)
    f.write(f"{len(viajes) + 1},{id_bus},{fecha},{hora},{origen},{destino},{tarifa}\n")
    f.close()
    return True


def mostrar_viaje(viaje):
    ciudades = cargar_ciudades()
    c_origen = obtener_ciudad(ciudades, viaje[4])
    c_destino = obtener_ciudad(ciudades, viaje[5])
    nombre_origen = viaje[4]
    nombre_destino = viaje[5]
    if c_origen is not None:
        nombre_origen = c_origen[1]
    if c_destino is not None:
        nombre_destino = c_destino[1]
    print(f"Viaje {viaje[0]} | Bus {viaje[1]} | {viaje[2]} {viaje[3]} | "
          f"{nombre_origen} -> {nombre_destino} | $ {viaje[6]}")


def listar_viajes():
    viajes = cargar_viajes()
    for v in viajes:
        mostrar_viaje(v)
    return len(viajes)


def consultar_viaje(id_viaje):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        return False
    mostrar_viaje(viaje)
    return True
