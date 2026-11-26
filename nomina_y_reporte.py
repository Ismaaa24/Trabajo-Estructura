from typing import Any, Dict, List, Optional, Tuple
from colorama import Fore, Style, init
from algoritmos import bubble_sort, busqueda_secuencial
from persistencia_benjamin import (
    cargar_buses_csv,
    cargar_ciudades_csv,
    cargar_clientes_csv,
    cargar_pasajes_csv,
    cargar_viajes_csv,
)
from reutilizacion_asientos import (
    obtener_ciudad_por_id_o_nombre,
    validar_sentido_tramo,
    verificar_reutilizacion_asiento,
)

init(autoreset=True)


def generar_nomina_viaje(
    id_viaje: str, criterio_orden: str
) -> Tuple[bool, str, List[Dict[str, Any]]]:
    viajes: List[Dict[str, Any]] = cargar_viajes_csv()
    viaje: Optional[Dict[str, Any]] = busqueda_secuencial(
        viajes, "id_viaje", id_viaje
    )
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", []

    pasajes: List[Dict[str, Any]] = cargar_pasajes_csv()
    clientes: List[Dict[str, str]] = cargar_clientes_csv()
    ciudades: List[Dict[str, Any]] = cargar_ciudades_csv()

    id_viaje_norm: str = str(id_viaje).strip().upper()
    nomina_sin_ordenar: List[Dict[str, Any]] = []

    for p in pasajes:
        if (
            str(p["id_viaje"]).strip().upper() == id_viaje_norm
            and str(p["estado"]).strip().upper() == "VIGENTE"
        ):
            cliente: Optional[Dict[str, Any]] = busqueda_secuencial(
                clientes, "id_cliente", p["id_cliente"]
            )
            c_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
                ciudades, p["id_origen"]
            )
            c_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
                ciudades, p["id_destino"]
            )

            ap_paterno: str = cliente["apellido_paterno"] if cliente else "Desconocido"
            ap_materno: str = cliente["apellido_materno"] if cliente else ""
            nombres: str = cliente["nombres"] if cliente else "Cliente"
            nombre_orig: str = c_orig["nombre"] if c_orig else str(p["id_origen"])
            nombre_dest: str = c_dest["nombre"] if c_dest else str(p["id_destino"])
            pos_orig: int = int(c_orig["posicion"]) if c_orig else 0

            nomina_sin_ordenar.append(
                {
                    "asiento": int(p["asiento"]),
                    "apellido_paterno": ap_paterno,
                    "apellido_materno": ap_materno,
                    "nombres": nombres,
                    "embarque": nombre_orig,
                    "destino_final": nombre_dest,
                    "pos_embarque": pos_orig,
                }
            )

    if not nomina_sin_ordenar:
        return True, "El viaje no tiene pasajes vigentes registrados.", []

    criterio: str = criterio_orden.strip().lower()
    if criterio == "a":
        nomina_ordenada: List[Dict[str, Any]] = bubble_sort(
            nomina_sin_ordenar,
            lambda x: (
                x["apellido_paterno"].lower(),
                x["apellido_materno"].lower(),
                x["nombres"].lower(),
                x["asiento"],
            ),
        )
    elif criterio == "b":
        nomina_ordenada = bubble_sort(
            nomina_sin_ordenar,
            lambda x: (
                x["nombres"].lower(),
                x["apellido_paterno"].lower(),
                x["apellido_materno"].lower(),
                x["asiento"],
            ),
        )
    elif criterio == "c":
        nomina_ordenada = bubble_sort(
            nomina_sin_ordenar,
            lambda x: (
                x["asiento"],
                x["pos_embarque"],
                x["apellido_paterno"].lower(),
            ),
        )
    else:
        return False, "Criterio de ordenamiento inválido. Use 'a', 'b' o 'c'.", []

    return True, "Nómina generada exitosamente.", nomina_ordenada


def obtener_reporte_pasajes_y_recaudacion(
    id_viaje: str,
) -> Tuple[bool, str, Dict[str, Any]]:
    viajes: List[Dict[str, Any]] = cargar_viajes_csv()
    viaje: Optional[Dict[str, Any]] = busqueda_secuencial(
        viajes, "id_viaje", id_viaje
    )
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", {}

    pasajes: List[Dict[str, Any]] = cargar_pasajes_csv()
    clientes: List[Dict[str, str]] = cargar_clientes_csv()
    ciudades: List[Dict[str, Any]] = cargar_ciudades_csv()

    id_viaje_norm: str = str(id_viaje).strip().upper()
    lista_pasajes: List[Dict[str, Any]] = []
    recaudacion_vigente: int = 0
    total_vigentes: int = 0
    total_anulados: int = 0

    for p in pasajes:
        if str(p["id_viaje"]).strip().upper() == id_viaje_norm:
            cliente: Optional[Dict[str, Any]] = busqueda_secuencial(
                clientes, "id_cliente", p["id_cliente"]
            )
            c_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
                ciudades, p["id_origen"]
            )
            c_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
                ciudades, p["id_destino"]
            )

            nombre_cli: str = (
                f"{cliente['nombres']} {cliente['apellido_paterno']}"
                if cliente
                else f"ID {p['id_cliente']}"
            )
            estado: str = str(p["estado"]).strip().upper()
            valor: int = int(p["valor"])

            if estado == "VIGENTE":
                recaudacion_vigente += valor
                total_vigentes += 1
            else:
                total_anulados += 1

            lista_pasajes.append(
                {
                    "id_pasaje": p["id_pasaje"],
                    "asiento": int(p["asiento"]),
                    "cliente": nombre_cli,
                    "origen": c_orig["nombre"] if c_orig else str(p["id_origen"]),
                    "destino": c_dest["nombre"] if c_dest else str(p["id_destino"]),
                    "valor": valor,
                    "estado": estado,
                }
            )

    reporte: Dict[str, Any] = {
        "pasajes": lista_pasajes,
        "recaudacion_vigente": recaudacion_vigente,
        "total_vigentes": total_vigentes,
        "total_anulados": total_anulados,
    }
    return True, "Reporte generado correctamente.", reporte


def consultar_ocupacion_por_tramo(
    id_viaje: str, id_origen: str, id_destino: str
) -> Tuple[bool, str, Dict[str, Any]]:
    viajes: List[Dict[str, Any]] = cargar_viajes_csv()
    viaje: Optional[Dict[str, Any]] = busqueda_secuencial(
        viajes, "id_viaje", id_viaje
    )
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", {}

    buses: List[Dict[str, Any]] = cargar_buses_csv()
    bus: Optional[Dict[str, Any]] = busqueda_secuencial(
        buses, "id_bus", viaje["id_bus"]
    )
    if bus is None:
        return False, "No se encontró el bus asignado al viaje.", {}

    ciudades: List[Dict[str, Any]] = cargar_ciudades_csv()
    c_v_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, viaje["id_origen"]
    )
    c_v_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, viaje["id_destino"]
    )
    c_p_orig: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, id_origen
    )
    c_p_dest: Optional[Dict[str, Any]] = obtener_ciudad_por_id_o_nombre(
        ciudades, id_destino
    )

    if not all([c_v_orig, c_v_dest, c_p_orig, c_p_dest]):
        return False, "Ciudad de origen o destino no válida.", {}

    assert c_v_orig is not None
    assert c_v_dest is not None
    assert c_p_orig is not None
    assert c_p_dest is not None

    if not validar_sentido_tramo(
        int(c_v_orig["posicion"]),
        int(c_v_dest["posicion"]),
        int(c_p_orig["posicion"]),
        int(c_p_dest["posicion"]),
    ):
        return False, "El tramo ingresado no respeta el sentido del viaje.", {}

    capacidad: int = int(bus["capacidad"])
    disponibles: List[int] = []
    ocupados: List[int] = []

    for asiento in range(1, capacidad + 1):
        libre, _ = verificar_reutilizacion_asiento(
            id_viaje, id_origen, id_destino, asiento
        )
        if libre:
            disponibles.append(asiento)
        else:
            ocupados.append(asiento)

    resultado: Dict[str, Any] = {
        "tramo": f"{c_p_orig['nombre']} -> {c_p_dest['nombre']}",
        "capacidad": capacidad,
        "disponibles": disponibles,
        "ocupados": ocupados,
    }
    return True, "Consulta realizada exitosamente.", resultado


def submenu_consultas_y_reportes() -> None:
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}--- CONSULTAS, NÓMINAS Y REPORTES ---{Style.RESET_ALL}")
        print("1. Nómina de pasajeros por viaje (RF08)")
        print("2. Listado general de clientes, buses y viajes programados (RF09)")
        print("3. Pasajes vigentes/anulados y recaudación vigente de un viaje (RF09)")
        print("4. Ocupación y disponibilidad de asientos por tramo (RF06 / RF09)")
        print("5. Volver")

        opcion: str = input("Ingrese una opción: ").strip()

        if opcion == "1":
            id_viaje: str = input("Ingrese ID del viaje: ").strip()
            print("Ordenar nómina por:")
            print("  (a) Apellido paterno alfabético ascendente")
            print("  (b) Nombres alfabético ascendente")
            print("  (c) Número de asiento numérico ascendente")
            criterio: str = input("Seleccione criterio (a/b/c): ").strip().lower()

            ok, msg, nomina = generar_nomina_viaje(id_viaje, criterio)
            if not ok:
                print(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}")
            elif not nomina:
                print(f"{Fore.YELLOW}[AVISO] {msg}{Style.RESET_ALL}")
            else:
                print(
                    f"\n{Fore.BLUE}{Style.BRIGHT}Asiento | Ap. Paterno    | Ap. Materno    | Nombres          | Embarque     | Destino Final{Style.RESET_ALL}"
                )
                print("-" * 92)
                for fila in nomina:
                    print(
                        f"{fila['asiento']:<7} | {fila['apellido_paterno']:<14} | "
                        f"{fila['apellido_materno']:<14} | {fila['nombres']:<16} | "
                        f"{fila['embarque']:<12} | {fila['destino_final']}"
                    )

        elif opcion == "2":
            clientes: List[Dict[str, str]] = cargar_clientes_csv()
            buses: List[Dict[str, Any]] = cargar_buses_csv()
            viajes: List[Dict[str, Any]] = cargar_viajes_csv()
            ciudades: List[Dict[str, Any]] = cargar_ciudades_csv()

            print(f"\n{Fore.CYAN}{Style.BRIGHT}=== CLIENTES REGISTRADOS ({len(clientes)}) ==={Style.RESET_ALL}")
            if not clientes:
                print(f"{Fore.YELLOW}[AVISO] Sin clientes registrados.{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}{Style.BRIGHT}ID   | RUT          | Nombre Completo                | Contacto{Style.RESET_ALL}")
                for c in clientes:
                    nombre_c: str = f"{c['nombres']} {c['apellido_paterno']} {c['apellido_materno']}"
                    print(f"{c['id_cliente']:<4} | {c['rut']:<12} | {nombre_c:<30} | {c['contacto']}")

            print(f"\n{Fore.CYAN}{Style.BRIGHT}=== BUSES REGISTRADOS ({len(buses)}) ==={Style.RESET_ALL}")
            if not buses:
                print(f"{Fore.YELLOW}[AVISO] Sin buses registrados.{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}{Style.BRIGHT}ID BUS   | Patente | Capacidad | Estado{Style.RESET_ALL}")
                for b in buses:
                    print(f"{b['id_bus']:<8} | {b['patente']:<7} | {b['capacidad']:<9} | {b['estado']}")

            print(f"\n{Fore.CYAN}{Style.BRIGHT}=== VIAJES PROGRAMADOS ({len(viajes)}) ==={Style.RESET_ALL}")
            if not viajes:
                print(f"{Fore.YELLOW}[AVISO] Sin viajes programados.{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}{Style.BRIGHT}ID VIAJE | Bus      | Fecha      | Hora  | Recorrido                 | Tarifa Base{Style.RESET_ALL}")
                for v in viajes:
                    c_o = obtener_ciudad_por_id_o_nombre(ciudades, v["id_origen"])
                    c_d = obtener_ciudad_por_id_o_nombre(ciudades, v["id_destino"])
                    n_o: str = c_o["nombre"] if c_o else str(v["id_origen"])
                    n_d: str = c_d["nombre"] if c_d else str(v["id_destino"])
                    print(
                        f"{v['id_viaje']:<8} | {v['id_bus']:<8} | {v['fecha']:<10} | "
                        f"{v['hora']:<5} | {n_o} -> {n_d:<12} | ${v['tarifa_base']:,}"
                    )

        elif opcion == "3":
            id_viaje = input("Ingrese ID del viaje: ").strip()
            ok, msg, rep = obtener_reporte_pasajes_y_recaudacion(id_viaje)
            if not ok:
                print(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}")
            else:
                print(
                    f"\n{Fore.BLUE}{Style.BRIGHT}ID Pasaje | Asiento | Cliente              | Tramo                     | Valor   | Estado{Style.RESET_ALL}"
                )
                print("-" * 92)
                for p in rep["pasajes"]:
                    tramo: str = f"{p['origen']} -> {p['destino']}"
                    color: str = Fore.GREEN if p["estado"] == "VIGENTE" else Fore.RED
                    print(
                        f"{p['id_pasaje']:<9} | {p['asiento']:<7} | {p['cliente']:<20} | "
                        f"{tramo:<25} | ${p['valor']:<6,} | {color}{p['estado']}{Style.RESET_ALL}"
                    )
                print("-" * 92)
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}[OK] Vigentes: {rep['total_vigentes']} | "
                    f"Anulados: {rep['total_anulados']} | "
                    f"Recaudación vigente: ${rep['recaudacion_vigente']:,} CLP{Style.RESET_ALL}"
                )

        elif opcion == "4":
            id_viaje = input("Ingrese ID del viaje: ").strip()
            ciudades = cargar_ciudades_csv()
            print(f"\n{Fore.BLUE}{Style.BRIGHT}ID | Ciudad       | Posición{Style.RESET_ALL}")
            for c in ciudades:
                print(f"{c['id_ciudad']:<2} | {c['nombre']:<12} | {c['posicion']}")

            id_orig: str = input("Ingrese ID o nombre ciudad de embarque: ").strip()
            id_dest: str = input("Ingrese ID o nombre ciudad de destino: ").strip()
            ok, msg, datos = consultar_ocupacion_por_tramo(id_viaje, id_orig, id_dest)
            if not ok:
                print(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}Tramo: {datos['tramo']} (Capacidad: {datos['capacidad']}){Style.RESET_ALL}")
                print(f"{Fore.GREEN}Disponibles ({len(datos['disponibles'])}): {datos['disponibles']}{Style.RESET_ALL}")
                print(f"{Fore.RED}Ocupados ({len(datos['ocupados'])}): {datos['ocupados']}{Style.RESET_ALL}")

        elif opcion == "5":
            print("Opción Finalizada")
            break
        else:
            print(f"{Fore.RED}Opción inválida, ingrese otra nuevamente.{Style.RESET_ALL}")