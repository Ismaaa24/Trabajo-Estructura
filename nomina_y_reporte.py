from algoritmos import bubble_sort, busqueda_secuencial
from persistencia import cargar_buses, cargar_ciudades, cargar_clientes
from persistencia import cargar_pasajes, cargar_viajes
from funciones_ciudad import obtener_ciudad
from reutilizacion_asientos import validar_sentido_tramo, verificar_reutilizacion_asiento


# Devuelve (ok, mensaje, nomina)
# cada fila de la nomina: [asiento, ap_paterno, ap_materno, nombres, embarque, destino, pos_embarque]
def generar_nomina_viaje(id_viaje, criterio):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", []

    pasajes = cargar_pasajes()
    clientes = cargar_clientes()
    ciudades = cargar_ciudades()

    nomina = []
    for p in pasajes:
        if p[1].upper() == id_viaje.strip().upper() and p[7].upper() == "VIGENTE":
            cliente = busqueda_secuencial(clientes, 0, p[2])
            c_origen = obtener_ciudad(ciudades, p[3])
            c_destino = obtener_ciudad(ciudades, p[4])

            ap_p = "Desconocido"
            ap_m = ""
            nombres = "Cliente"
            if cliente is not None:
                nombres = cliente[2]
                ap_p = cliente[3]
                ap_m = cliente[4]

            embarque = p[3]
            pos_embarque = 0
            if c_origen is not None:
                embarque = c_origen[1]
                pos_embarque = c_origen[2]
            destino = p[4]
            if c_destino is not None:
                destino = c_destino[1]

            nomina.append([p[5], ap_p, ap_m, nombres, embarque, destino, pos_embarque])

    if len(nomina) == 0:
        return True, "El viaje no tiene pasajes vigentes registrados.", []

    criterio = criterio.strip().lower()
    if criterio == "a":
        ordenada = bubble_sort(nomina, [1, 2, 3, 0])   # ap. paterno
    elif criterio == "b":
        ordenada = bubble_sort(nomina, [3, 1, 2, 0])   # nombres
    elif criterio == "c":
        ordenada = bubble_sort(nomina, [0, 6, 1])      # asiento
    else:
        return False, "Criterio de ordenamiento inválido. Use 'a', 'b' o 'c'.", []

    return True, "Nómina generada exitosamente.", ordenada


# Devuelve (ok, mensaje, lista_pasajes, recaudacion_vigente, total_vigentes, total_anulados)
def obtener_reporte_pasajes_y_recaudacion(id_viaje):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", [], 0, 0, 0

    clientes = cargar_clientes()
    ciudades = cargar_ciudades()

    lista = []
    recaudacion = 0
    vigentes = 0
    anulados = 0

    for p in cargar_pasajes():
        if p[1].upper() == id_viaje.strip().upper():
            cliente = busqueda_secuencial(clientes, 0, p[2])
            c_origen = obtener_ciudad(ciudades, p[3])
            c_destino = obtener_ciudad(ciudades, p[4])

            nombre = "ID " + p[2]
            if cliente is not None:
                nombre = cliente[2] + " " + cliente[3]
            origen = p[3]
            if c_origen is not None:
                origen = c_origen[1]
            destino = p[4]
            if c_destino is not None:
                destino = c_destino[1]

            estado = p[7].upper()
            if estado == "VIGENTE":
                recaudacion = recaudacion + p[6]
                vigentes = vigentes + 1
            else:
                anulados = anulados + 1

            lista.append([p[0], p[5], nombre, origen, destino, p[6], estado])

    return True, "Reporte generado correctamente.", lista, recaudacion, vigentes, anulados


# Devuelve (ok, mensaje, tramo, capacidad, disponibles, ocupados)
def consultar_ocupacion_por_tramo(id_viaje, id_origen, id_destino):
    viaje = busqueda_secuencial(cargar_viajes(), 0, id_viaje)
    if viaje is None:
        return False, f"No existe el viaje con ID '{id_viaje}'.", "", 0, [], []

    bus = busqueda_secuencial(cargar_buses(), 0, viaje[1])
    if bus is None:
        return False, "No se encontró el bus asignado al viaje.", "", 0, [], []

    ciudades = cargar_ciudades()
    c_v_origen = obtener_ciudad(ciudades, viaje[4])
    c_v_destino = obtener_ciudad(ciudades, viaje[5])
    c_p_origen = obtener_ciudad(ciudades, id_origen)
    c_p_destino = obtener_ciudad(ciudades, id_destino)

    if c_v_origen is None or c_v_destino is None or c_p_origen is None or c_p_destino is None:
        return False, "Ciudad de origen o destino no válida.", "", 0, [], []

    if not validar_sentido_tramo(c_v_origen[2], c_v_destino[2], c_p_origen[2], c_p_destino[2]):
        return False, "El tramo ingresado no respeta el sentido del viaje.", "", 0, [], []

    capacidad = bus[2]
    disponibles = []
    ocupados = []
    for asiento in range(1, capacidad + 1):
        libre, mensaje = verificar_reutilizacion_asiento(id_viaje, id_origen, id_destino, asiento)
        if libre:
            disponibles.append(asiento)
        else:
            ocupados.append(asiento)

    tramo = c_p_origen[1] + " -> " + c_p_destino[1]
    return True, "Consulta realizada exitosamente.", tramo, capacidad, disponibles, ocupados


def submenu_consultas_y_reportes():
    while True:
        print("\n--- CONSULTAS, NÓMINAS Y REPORTES ---")
        print("1. Nómina de pasajeros por viaje")
        print("2. Listado general de clientes, buses y viajes programados")
        print("3. Pasajes vigentes/anulados y recaudación vigente de un viaje")
        print("4. Ocupación y disponibilidad de asientos por tramo")
        print("5. Volver")

        opcion = input("Ingrese una opción: ").strip()

        if opcion == "1":
            id_viaje = input("Ingrese ID del viaje: ").strip()
            print("Ordenar nómina por:")
            print("  (a) Apellido paterno alfabético ascendente")
            print("  (b) Nombres alfabético ascendente")
            print("  (c) Número de asiento numérico ascendente")
            criterio = input("Seleccione criterio (a/b/c): ").strip().lower()

            ok, msg, nomina = generar_nomina_viaje(id_viaje, criterio)
            if not ok:
                print("[ERROR]", msg)
            elif len(nomina) == 0:
                print("[AVISO]", msg)
            else:
                print("\nAsiento | Ap. Paterno    | Ap. Materno    | Nombres          | Embarque     | Destino Final")
                print("-" * 92)
                for fila in nomina:
                    print(f"{fila[0]:<7} | {fila[1]:<14} | {fila[2]:<14} | "
                          f"{fila[3]:<16} | {fila[4]:<12} | {fila[5]}")

        elif opcion == "2":
            clientes = cargar_clientes()
            buses = cargar_buses()
            viajes = cargar_viajes()
            ciudades = cargar_ciudades()

            print(f"\n=== CLIENTES REGISTRADOS ({len(clientes)}) ===")
            if len(clientes) == 0:
                print("[AVISO] Sin clientes registrados.")
            else:
                print("ID   | RUT          | Nombre Completo                | Contacto")
                for c in clientes:
                    nombre = c[2] + " " + c[3] + " " + c[4]
                    print(f"{c[0]:<4} | {c[1]:<12} | {nombre:<30} | {c[5]}")

            print(f"\n=== BUSES REGISTRADOS ({len(buses)}) ===")
            if len(buses) == 0:
                print("[AVISO] Sin buses registrados.")
            else:
                print("ID BUS   | Patente | Capacidad | Estado")
                for b in buses:
                    print(f"{b[0]:<8} | {b[1]:<7} | {b[2]:<9} | {b[3]}")

            print(f"\n=== VIAJES PROGRAMADOS ({len(viajes)}) ===")
            if len(viajes) == 0:
                print("[AVISO] Sin viajes programados.")
            else:
                print("ID VIAJE | Bus      | Fecha      | Hora  | Recorrido                 | Tarifa Base")
                for v in viajes:
                    c_o = obtener_ciudad(ciudades, v[4])
                    c_d = obtener_ciudad(ciudades, v[5])
                    nombre_o = v[4]
                    nombre_d = v[5]
                    if c_o is not None:
                        nombre_o = c_o[1]
                    if c_d is not None:
                        nombre_d = c_d[1]
                    print(f"{v[0]:<8} | {v[1]:<8} | {v[2]:<10} | {v[3]:<5} | "
                          f"{nombre_o} -> {nombre_d:<12} | ${v[6]:,}")

        elif opcion == "3":
            id_viaje = input("Ingrese ID del viaje: ").strip()
            ok, msg, lista, recaudacion, vigentes, anulados = obtener_reporte_pasajes_y_recaudacion(id_viaje)
            if not ok:
                print("[ERROR]", msg)
            else:
                print("\nID Pasaje | Asiento | Cliente              | Tramo                     | Valor   | Estado")
                print("-" * 92)
                for p in lista:
                    tramo = p[3] + " -> " + p[4]
                    print(f"{p[0]:<9} | {p[1]:<7} | {p[2]:<20} | {tramo:<25} | ${p[5]:<6,} | {p[6]}")
                print("-" * 92)
                print(f"[OK] Vigentes: {vigentes} | Anulados: {anulados} | "
                      f"Recaudación vigente: ${recaudacion:,} CLP")

        elif opcion == "4":
            id_viaje = input("Ingrese ID del viaje: ").strip()
            ciudades = cargar_ciudades()
            print("\nID | Ciudad       | Posición")
            for c in ciudades:
                print(f"{c[0]:<2} | {c[1]:<12} | {c[2]}")

            id_orig = input("Ingrese ID o nombre ciudad de embarque: ").strip()
            id_dest = input("Ingrese ID o nombre ciudad de destino: ").strip()
            ok, msg, tramo, capacidad, disponibles, ocupados = consultar_ocupacion_por_tramo(id_viaje, id_orig, id_dest)
            if not ok:
                print("[ERROR]", msg)
            else:
                print(f"\nTramo: {tramo} (Capacidad: {capacidad})")
                print(f"Disponibles ({len(disponibles)}): {disponibles}")
                print(f"Ocupados ({len(ocupados)}): {ocupados}")

        elif opcion == "5":
            print("Opción Finalizada")
            break
        else:
            print("Opción inválida, ingrese otra nuevamente.")
