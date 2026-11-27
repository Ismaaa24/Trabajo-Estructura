from reutilizacion_asientos import verificar_reutilizacion_asiento
from funciones_clientes import buscar_cliente
from funciones_viajes import leer_archivo
from config import ARCHIVO_PASAJES, ENCODE


def vender_pasaje(id_viaje: str, rut: str, origen: int, destino: int, asiento: int) -> bool:
    viaje = None
    for v in leer_archivo("viajes.csv"):
        if v[0] == id_viaje:
            viaje = v
    if viaje is None:
        print("El viaje no existe")
        return False

    cliente = buscar_cliente(rut)
    if cliente is None:
        print("El cliente no existe")
        return False

    disponible, mensaje = verificar_reutilizacion_asiento(
        id_viaje, str(origen), str(destino), asiento
    )
    if not disponible:
        print(mensaje)
        return False

    # Precio: 10% de descuento por cada segmento (de 5) que no se usa
    segmentos_usados = abs(destino - origen)
    descuento = (5 - segmentos_usados) * 10
    precio = int(int(viaje[6]) * (100 - descuento) / 100)

    pasajes = leer_archivo("pasajes.csv")
    id_cliente = cliente[0].strip()
    f = open("pasajes.csv", "a", encoding="UTF-8")
    f.write(f"{len(pasajes) + 1},{id_viaje},{id_cliente},{origen},{destino},{asiento},{precio},VIGENTE\n")
    f.close()
    return True

def anular_pasaje(id_pasaje: str) -> bool:
    try:
        f = open(ARCHIVO_PASAJES, "r", encoding=ENCODE)
        lineas = f.readlines()
        f.close()
    except FileNotFoundError:
        print("Todavía no hay pasajes registrados.")
        return False

    for i in range(len(lineas)):
        datos = lineas[i].strip().split(",")

        if datos[0].strip() == id_pasaje:
            if len(datos) != 8:
                print("La fila de este pasaje tiene un formato incorrecto.")
                return False

            estado = datos[7].strip().upper()

            if estado == "ANULADO":
                print("Este pasaje ya fue anulado.")
                return False

            if estado != "VIGENTE":
                print("El estado del pasaje es inválido.")
                return False

            datos[7] = "ANULADO"
            lineas[i] = ",".join(datos) + "\n"

            try:
                f = open(ARCHIVO_PASAJES, "w", encoding=ENCODE)
                f.writelines(lineas)
                f.close()
            except OSError as error:
                print(f"No se pudo guardar la anulación: {error}")
                return False

            return True

    print("Pasaje no encontrado.")
    return False