from config import ARCHIVO_CIUDADES, ENCODE


def listar_ciudades() -> None:
    try:
        f = open(ARCHIVO_CIUDADES, "r", encoding=ENCODE)
    except FileNotFoundError:
        print(f"No se encontró el archivo de ciudades: {ARCHIVO_CIUDADES}")
        return

    lista = f.readlines()
    f.close()

    print(f"{'POSICIÓN':<10} {'ID':<10} CIUDAD")

    for registro in lista[1:]:
        if registro.strip() == "":
            continue

        id_ciudad, nombre, posicion = registro.strip().split(",")
        print(f"{posicion.strip():<10} {id_ciudad.strip():<10} {nombre.strip()}")