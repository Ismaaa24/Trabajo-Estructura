from clientes import buscar_cliente
from viajes import leer_archivo


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

    if origen < 0 or origen > 5 or destino < 0 or destino > 5:
        print("Ciudad inválida")
        return False

    # El tramo debe ir en el mismo sentido que el viaje
    if int(viaje[4]) == 0:
        sentido_correcto = origen < destino
    else:
        sentido_correcto = origen > destino
    if not sentido_correcto:
        print("El tramo no respeta el sentido del viaje")
        return False

    capacidad = 0
    for b in leer_archivo("buses.csv"):
        if b[0] == viaje[1]:
            capacidad = int(b[2])
    if asiento < 1 or asiento > capacidad:
        print("El asiento está fuera de la capacidad del bus")
        return False

    # Precio: 10% de descuento por cada segmento (de 5) que no se usa
    segmentos_usados = abs(destino - origen)
    descuento = (5 - segmentos_usados) * 10
    precio = int(int(viaje[6]) * (100 - descuento) / 100)

    pasajes = leer_archivo("pasajes.csv")
    id_cliente = cliente[0].split(":")[1].strip()
    f = open("pasajes.csv", "a", encoding="UTF-8")
    f.write(f"{len(pasajes) + 1},{id_viaje},{id_cliente},{origen},{destino},{asiento},{precio},VIGENTE\n")
    f.close()
    return True