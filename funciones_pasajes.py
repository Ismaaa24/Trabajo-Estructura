from config import ARCHIVO_PASAJES, ENCODE
from algoritmos import busqueda_secuencial
from persistencia import cargar_viajes, cargar_pasajes
from funciones_clientes import buscar_cliente
from reutilizacion_asientos import verificar_reutilizacion_asiento


def vender_pasaje(id_viaje, rut, origen, destino, asiento):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        print("El viaje no existe")
        return False

    cliente = buscar_cliente(rut)
    if cliente is None:
        print("El cliente no existe")
        return False

    disponible, mensaje = verificar_reutilizacion_asiento(id_viaje, str(origen), str(destino), asiento)
    if not disponible:
        print(mensaje)
        return False

    # Precio: 10% de descuento por cada segmento (de 5) que no se usa
    segmentos_usados = abs(destino - origen)
    descuento = (5 - segmentos_usados) * 10
    precio = int(viaje[6] * (100 - descuento) / 100)

    pasajes = cargar_pasajes()
    f = open(ARCHIVO_PASAJES, "a", encoding=ENCODE)
    f.write(f"{len(pasajes) + 1},{viaje[0]},{cliente[0]},{origen},{destino},{asiento},{precio},VIGENTE\n")
    f.close()
    return True


def anular_pasaje(id_pasaje):
    try:
        f = open(ARCHIVO_PASAJES, "r", encoding=ENCODE)
    except FileNotFoundError:
        print("Todavía no hay pasajes registrados.")
        return False
    lineas = f.readlines()
    f.close()

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
            f = open(ARCHIVO_PASAJES, "w", encoding=ENCODE)
            f.writelines(lineas)
            f.close()
            return True

    print("Pasaje no encontrado.")
    return False
