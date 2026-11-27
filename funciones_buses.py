import os
from config import ARCHIVO_BUSES, ENCODE
from algoritmos import busqueda_secuencial
from persistencia import cargar_buses


def listar_buses():
    buses = cargar_buses()
    print(f"{'ID BUS':<10} {'PATENTE':<10} {'CAPACIDAD':<10} ESTADO")
    for b in buses:
        print(f"{b[0]:<10} {b[1]:<10} {b[2]:<10} {b[3]}")


def pedir_id_bus(mensaje):
    while True:
        id_bus = input(mensaje).strip().upper()
        if id_bus == "":
            print("El ID del bus no puede estar vacio.")
        elif not id_bus.startswith("BUS_") or not id_bus[4:].isdigit():
            print("Use el formato BUS_ seguido de numeros, por ejemplo BUS_01")
        else:
            return id_bus


def registrar_buses():
    id_bus = pedir_id_bus("Ingrese el ID del bus: ")

    while True:
        patente = input("Ingrese la patente del bus: ").strip().upper()
        if patente == "":
            print("La patente no puede estar vacia.")
        elif len(patente) != 6 or patente[3] != "-":
            print("Use el formato de patente ABC-12")
        elif not patente[:3].isalpha() or not patente[4:].isdigit():
            print("Ingrese tres letras, un guion y dos numeros.")
        else:
            break

    while True:
        capacidad = input("Ingrese la capacidad del bus: ")
        if not capacidad.isdigit():
            print("Ingrese un numero entero, por ejemplo 30.")
        elif int(capacidad) <= 0:
            print("La capacidad debe ser mayor que 0.")
        else:
            capacidad = int(capacidad)
            break

    while True:
        estado = input("Ingrese el estado del bus (DISPONIBLE / NO DISPONIBLE): ").strip().upper()
        if estado == "DISPONIBLE" or estado == "NO DISPONIBLE":
            break
        print("El estado debe ser DISPONIBLE o NO DISPONIBLE")

    buses = cargar_buses()
    if busqueda_secuencial(buses, 0, id_bus) is not None:
        print("Ya existe un bus con esa ID.")
        return
    if busqueda_secuencial(buses, 1, patente) is not None:
        print("Ya existe un bus con esa patente.")
        return

    archivo_nuevo = not os.path.exists(ARCHIVO_BUSES) or os.path.getsize(ARCHIVO_BUSES) == 0
    f = open(ARCHIVO_BUSES, "a", encoding=ENCODE)
    if archivo_nuevo:
        f.write("id_bus,patente,capacidad,estado\n")
    f.write(f"{id_bus},{patente},{capacidad},{estado}\n")
    f.close()
    print("Bus registrado exitosamente!")


def consultar_bus():
    id_buscado = pedir_id_bus("Ingrese el ID del Bus a consultar: ")
    print(f"Buscando {id_buscado}...\n")

    bus = busqueda_secuencial(cargar_buses(), 0, id_buscado)
    if bus is None:
        print("Bus no encontrado")
    else:
        print("---Bus Encontrado---")
        print(f"ID: {bus[0]}")
        print(f"Patente: {bus[1]}")
        print(f"Capacidad: {bus[2]}")
        print(f"Estado: {bus[3]}")
