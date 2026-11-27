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
    except Exception:
        pass
    return filas

def registrar_viaje(id_bus: str, fecha: str, hora: str, id_origen: int, id_destino: int, tarifa_base: int) -> bool:
    bus_existe = False
    for b in leer_archivo("buses.csv"):
        if b[0] == id_bus:
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

    viajes = leer_archivo("viajes.csv")
    for v in viajes:
        if v[1] == id_bus and v[2] == fecha and v[3] == hora:
            print("El bus ya tiene un viaje a esa fecha y hora")
            return False

    f = open("viajes.csv", "a", encoding="UTF-8")
    f.write(f"{len(viajes) + 1},{id_bus},{fecha},{hora},{id_origen},{id_destino},{tarifa_base}\n")
    f.close()
    return True

def listar_viajes() -> None:
    for v in leer_archivo("viajes.csv"):
        print(v[0], v[2], v[3], CIUDADES[int(v[4])], "->", CIUDADES[int(v[5])], "$" + v[6])