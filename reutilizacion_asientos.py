from algoritmos import busqueda_secuencial
from persistencia import cargar_buses, cargar_ciudades, cargar_pasajes, cargar_viajes
from funciones_ciudad import obtener_ciudad


# El tramo del pasajero debe ir dentro del recorrido del viaje y en el mismo sentido
def validar_sentido_tramo(v_origen, v_destino, p_origen, p_destino):
    if p_origen == p_destino:
        return False
    if v_origen < v_destino:
        return v_origen <= p_origen < p_destino <= v_destino
    if v_origen > v_destino:
        return v_origen >= p_origen > p_destino >= v_destino
    return False


# Dos tramos se superponen si comparten algun segmento del recorrido
def tramos_se_superponen(a_origen, a_destino, b_origen, b_destino):
    min_a = min(a_origen, a_destino)
    max_a = max(a_origen, a_destino)
    min_b = min(b_origen, b_destino)
    max_b = max(b_origen, b_destino)
    return max(min_a, min_b) < min(max_a, max_b)


# Devuelve (True/False, mensaje)
def verificar_reutilizacion_asiento(id_viaje, origen_pasajero, destino_pasajero, asiento):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        return False, "El viaje especificado no existe."

    bus = busqueda_secuencial(cargar_buses(), 0, viaje[1])
    if bus is None:
        return False, "El bus asociado al viaje no existe."

    capacidad = bus[2]
    if asiento < 1 or asiento > capacidad:
        return False, f"El asiento debe estar entre 1 y {capacidad}."

    ciudades = cargar_ciudades()
    c_v_origen = obtener_ciudad(ciudades, viaje[4])
    c_v_destino = obtener_ciudad(ciudades, viaje[5])
    c_p_origen = obtener_ciudad(ciudades, origen_pasajero)
    c_p_destino = obtener_ciudad(ciudades, destino_pasajero)

    if c_v_origen is None or c_v_destino is None or c_p_origen is None or c_p_destino is None:
        return False, "Una o más ciudades ingresadas no son válidas."

    if not validar_sentido_tramo(c_v_origen[2], c_v_destino[2], c_p_origen[2], c_p_destino[2]):
        return False, "El tramo no es válido o no respeta el sentido del viaje."

    # se revisan los pasajes vigentes del mismo viaje y asiento
    for pasaje in cargar_pasajes():
        if pasaje[1].upper() != str(id_viaje).strip().upper():
            continue
        if pasaje[7].upper() != "VIGENTE":
            continue
        if pasaje[5] != asiento:
            continue
        c_o = obtener_ciudad(ciudades, pasaje[3])
        c_d = obtener_ciudad(ciudades, pasaje[4])
        if c_o is not None and c_d is not None:
            if tramos_se_superponen(c_p_origen[2], c_p_destino[2], c_o[2], c_d[2]):
                return False, (f"Asiento {asiento} ocupado en tramo superpuesto "
                               f"({c_o[1]} -> {c_d[1]}).")

    return True, f"Asiento {asiento} disponible para el tramo solicitado."
