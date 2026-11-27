from typing import Any, Dict, List, Optional, Tuple
from algoritmos import busqueda_secuencial
from persistencia_benjamin import (
    cargar_buses_csv,
    cargar_ciudades_csv,
    cargar_pasajes_csv,
    cargar_viajes_csv,
)


def obtener_ciudad_por_id_o_nombre(
    ciudades: List[Dict[str, Any]], valor: str
) -> Optional[Dict[str, Any]]:
    encontrada: Optional[Dict[str, Any]] = busqueda_secuencial(
        ciudades, "id_ciudad", valor
    )
    if encontrada is not None:
        return encontrada
    return busqueda_secuencial(ciudades, "nombre", valor)


def validar_sentido_tramo(
    pos_viaje_origen: int,
    pos_viaje_destino: int,
    pos_pasajero_origen: int,
    pos_pasajero_destino: int,
) -> bool:
    if pos_pasajero_origen == pos_pasajero_destino:
        return False
    if pos_viaje_origen < pos_viaje_destino:
        return (
            pos_viaje_origen
            <= pos_pasajero_origen
            < pos_pasajero_destino
            <= pos_viaje_destino
        )
    if pos_viaje_origen > pos_viaje_destino:
        return (
            pos_viaje_origen
            >= pos_pasajero_origen
            > pos_pasajero_destino
            >= pos_viaje_destino
        )
    return False


def tramos_se_superponen(
    pos_a_origen: int,
    pos_a_destino: int,
    pos_b_origen: int,
    pos_b_destino: int,
) -> bool:
    min_a: int = min(pos_a_origen, pos_a_destino)
    max_a: int = max(pos_a_origen, pos_a_destino)
    min_b: int = min(pos_b_origen, pos_b_destino)
    max_b: int = max(pos_b_origen, pos_b_destino)
    return max(min_a, min_b) < min(max_a, max_b)


def verificar_reutilizacion_asiento(
    id_viaje: str,
    id_origen_pasajero: str,
    id_destino_pasajero: str,
    asiento: int,
) -> Tuple[bool, str]:
    viajes: List[Dict[str, Any]] = cargar_viajes_csv()
    viaje: Optional[Dict[str, Any]] = busqueda_secuencial(
        viajes, "id_viaje", id_viaje
    )
    if viaje is None:
        return False, "El viaje especificado no existe."

    buses: List[Dict[str, Any]] = cargar_buses_csv()
    bus: Optional[Dict[str, Any]] = busqueda_secuencial(
        buses, "id_bus", viaje["id_bus"]
    )
    if bus is None:
        return False, "El bus asociado al viaje no existe."

    capacidad: int = int(bus["capacidad"])
    if asiento < 1 or asiento > capacidad:
        return False, f"El asiento debe estar entre 1 y {capacidad}."

    ciudades: List[Dict[str, Any]] = cargar_ciudades_csv()
    c_viaje_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, viaje["id_origen"]
    )
    c_viaje_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, viaje["id_destino"]
    )
    c_pas_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, id_origen_pasajero
    )
    c_pas_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, id_destino_pasajero
    )

    if not all([c_viaje_orig, c_viaje_dest, c_pas_orig, c_pas_dest]):
        return False, "Una o más ciudades ingresadas no son válidas."

    assert c_viaje_orig is not None
    assert c_viaje_dest is not None
    assert c_pas_orig is not None
    assert c_pas_dest is not None

    pos_v_orig: int = int(c_viaje_orig["posicion"])
    pos_v_dest: int = int(c_viaje_dest["posicion"])
    pos_p_orig: int = int(c_pas_orig["posicion"])
    pos_p_dest: int = int(c_pas_dest["posicion"])

    if not validar_sentido_tramo(pos_v_orig, pos_v_dest, pos_p_orig, pos_p_dest):
        return (
            False,
            "El tramo no es válido o no respeta el sentido del viaje.",
        )

    pasajes: List[Dict[str, Any]] = cargar_pasajes_csv()
    id_viaje_norm: str = str(id_viaje).strip().upper()

    for pasaje in pasajes:
        if str(pasaje["id_viaje"]).strip().upper() != id_viaje_norm:
            continue
        if str(pasaje["estado"]).strip().upper() != "VIGENTE":
            continue
        if int(pasaje["asiento"]) != asiento:
            continue

        c_ocup_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
            ciudades, pasaje["id_origen"]
        )
        c_ocup_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
            ciudades, pasaje["id_destino"]
        )
        if c_ocup_orig is not None and c_ocup_dest is not None:
            if tramos_se_superponen(
                pos_p_orig,
                pos_p_dest,
                int(c_ocup_orig["posicion"]),
                int(c_ocup_dest["posicion"]),
            ):
                return (
                    False,
                    f"Asiento {asiento} ocupado en tramo superpuesto "
                    f"({c_ocup_orig['nombre']} -> {c_ocup_dest['nombre']}).",
                )

    return True, f"Asiento {asiento} disponible para el tramo solicitado."