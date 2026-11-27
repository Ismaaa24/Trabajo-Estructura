from nomina_y_reporte import submenu_consultas_y_reportes
from config import ARCHIVO_BUSES, ARCHIVO_CIUDADES, ENCODE
from funciones_buses import listar_buses, registrar_buses, consultar_bus
from funciones_clientes import registrar_cliente, lista_De_clientes, listar_clientes, buscar_cliente, pedir_id_cliente, pedir_texto
from funciones_ciudad import listar_ciudades
from funciones_pasajes import vender_pasaje, anular_pasaje
from funciones_viajes import registrar_viaje, listar_viajes, consultar_viaje

while True:
    print("""
----MENU INTERACTIVO----
1. Clientes
2. Buses 
3. Ciudades
4. Viajes
5. Pasajes
6. Consultas y Reportes
0. Finalizar Programa""")
    
    op = input("Ingrese una opcion: ")
    
    if op == "1":
        while True:
            print("""
--Opciones Clientes--
1. Registrar Cliente
2. Listar Cliente
3. Buscar Cliente
4. Volver """)
            
            op_clientes = input("Ingrese una opcion: ")
            
            if op_clientes == "1":
                rut = pedir_texto("el RUT").upper()
                if buscar_cliente(rut) is not None:
                    print("Cliente ya registrado.")
                    continue
                nombre = pedir_texto("el nombre")
                apellido_p = pedir_texto("el apellido paterno")
                apellido_m = pedir_texto("el apellido materno")
                contacto = pedir_texto("el contacto")
                clientes = lista_De_clientes()
                id_cliente = max((int(c[0]) for c in clientes), default=100) + 1
                registrar_cliente(id_cliente, rut, nombre, apellido_p, apellido_m, contacto)
                print("Cliente registrado.")
            if op_clientes == "2":
                listar_clientes()
            if op_clientes == "3":
                
                buscar = pedir_texto("el RUT a buscar").upper()
                respuesta = buscar_cliente(buscar)
                if respuesta is not None:
                    print(respuesta)
                else:
                    print("Cliente no encontrado.")
                    
            if op_clientes == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "2":
        while True:
            print("""
---Opciones Buses---
1. Registrar Buses
2. Listar Bus
3. Consultar Bus
4. Volver """)
            
            op_buses = input("Ingrese una opcion: ")
            
            if op_buses == "1":
                registrar_buses()
            if op_buses == "2":
                listar_buses()
            if op_buses == "3":
                consultar_bus()
            if op_buses == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "3":
        listar_ciudades()
    
    elif op == "4":
        while True:
            print("""
  ---Opciones Viajes---
1. Programar Viaje.
2. Listar Viajes Programados.
3. Consultar un viaje.
4. Volver. """)
            
            op_viaje = input("Ingrese una opcion: ")
            
            if op_viaje == "1":
                id_bus = pedir_texto("el ID del bus").upper()
                fecha = pedir_texto("la fecha del viaje (DD/MM/AAAA)")
                hora = pedir_texto("la hora de salida (HH:MM)")

                listar_ciudades()
                try:
                    origen = int(input("Ingrese la posición de origen: "))
                    destino = int(input("Ingrese la posición de destino: "))
                    tarifa = int(input("Ingrese la tarifa base en pesos: "))
                except ValueError:
                    print("El origen, el destino y la tarifa deben ser números enteros.")
                    continue

                guardado = registrar_viaje(id_bus, fecha, hora, origen, destino, tarifa)

                if guardado:
                    print("Viaje registrado correctamente.")
                    
            if op_viaje == "2":
                cantidad = listar_viajes()
                if cantidad == 0:
                    print("No hay viajes programados.")
            if op_viaje == "3":
                id_viaje = pedir_texto("el ID del viaje")
                if not consultar_viaje(id_viaje):
                    print("Viaje no encontrado.")
            if op_viaje == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "5":
        while True:
            print("""
---Opciones Pasajes---
1. Venta de pasajes
2. Anulacion de pasajes
3. Buscar Cliente
4. Volver """)
            
            op_pasajes = input("Ingrese una opcion: ")
            
            if op_pasajes == "1":
                if listar_viajes() == 0:
                    print("Primero debe programar un viaje.")
                    continue
                id_viaje = pedir_texto("el ID del viaje")
                rut = pedir_texto("el RUT del cliente").upper()

                listar_ciudades()
                try:
                    origen = int(input("Ingrese la posición donde sube el pasajero: "))
                    destino = int(input("Ingrese la posición donde baja el pasajero: "))
                    asiento = int(input("Ingrese el número de asiento: "))
                except ValueError:
                    print("El origen, el destino y el asiento deben ser números enteros.")
                    continue

                vendido = vender_pasaje(id_viaje, rut, origen, destino, asiento)
                if vendido:
                    print("Pasaje vendido correctamente.")
            if op_pasajes == "2":
                id_pasaje = pedir_texto("el ID del pasaje a anular")
                anulado = anular_pasaje(id_pasaje)

                if anulado:
                    print("Pasaje anulado correctamente.")
            if op_pasajes == "3":
                rut = pedir_texto("el RUT del cliente a buscar").upper()
                cliente = buscar_cliente(rut)

                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print(f"Cliente encontrado: {cliente[2].strip()} "
                          f"{cliente[3].strip()} {cliente[4].strip()}")
            if op_pasajes == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "6":
        submenu_consultas_y_reportes()
    elif op == "0":
        print("Programa finalizado")
        break
    else:
        print("Opcion Invalida, Ingrese otra nuevamente. ")
            
    