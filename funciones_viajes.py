from datetime import datetime

CIUDADES = ["Concepción", "Chillán", "Linares", "Talca", "Rancagua", "Santiago"]

def leer_archivo(ruta: str) -> list:
    """Lee un archivo CSV y devuelve sus filas como listas."""
    filas = []
    try:
        f = open(ruta, "r", encoding="UTF-8")
        for linea in f:
            if linea.strip() != "":
                filas.append(linea.strip().split(","))
        f.close()
    except FileNotFoundError:
        pass
    return filas

def registrar_viaje(id_bus: str, fecha: str, hora: str, id_origen: int, id_destino: int, tarifa_base: int) -> bool:
    bus_existe = False
    for b in leer_archivo("buses.csv"):
        if b[0].strip().upper() == id_bus:
            if b[3].strip().upper() == "NO DISPONIBLE":
                print("El bus no está disponible.")
                return False
            bus_existe = True
    if not bus_existe:
        print("El bus no existe")
        return False

    if not ((id_origen == 0 and id_destino == 5) or (id_origen == 5 and id_destino == 0)):
        print("Solo se programan viajes Concepción-Santiago o Santiago-Concepción")
        return False

    if len(fecha) != 10 or len(hora) != 5 or tarifa_base <= 0:
        print("Fecha, hora o tarifa inválidas")
        return False

    try:
        datetime.strptime(fecha + " " + hora, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Fecha u hora inválida.")
        return False

    viajes = leer_archivo("viajes.csv")
    for v in viajes:
        if v[1] == id_bus and v[2] == fecha and v[3] == hora:
            print("El bus ya tiene un viaje a esa fecha y hora")
            return False

    f = open("viajes.csv", "a", encoding="UTF-8")
    f.write(f"{len(viajes) + 1},{id_bus},{fecha},{hora},{id_origen},{id_destino},{tarifa_base}\n")
    f.close()
    return True

def mostrar_viaje(viaje: list) -> None:
    id_viaje, id_bus, fecha, hora, origen, destino, tarifa = viaje
    print(f"Viaje {id_viaje} | Bus {id_bus} | {fecha} {hora} | "
          f"{CIUDADES[int(origen)]} -> {CIUDADES[int(destino)]} | $ {tarifa}")


def listar_viajes() -> int:
    viajes = leer_archivo("viajes.csv")
    for viaje in viajes:
        mostrar_viaje(viaje)
    return len(viajes)


def consultar_viaje(id_viaje: str) -> bool:
    for viaje in leer_archivo("viajes.csv"):
        if viaje[0] == id_viaje:
            mostrar_viaje(viaje)
            return True
    return False
