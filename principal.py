from config import ARCHIVO_BUSES, ARCHIVO_CIUDADES, ENCODE
from funciones_buses import listar_buses, registrar_buses, consultar_bus
from funciones_clientes import registrar_cliente, lista_De_clientes, listar_clientes, buscar_cliente, pedir_id_cliente, pedir_texto
from funciones_ciudades import listar_ciudades

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
                id_cliente = pedir_id_cliente()
                rut = pedir_texto("el RUT").upper()
                nombre = pedir_texto("el nombre")
                apellido_p = pedir_texto("el apellido paterno")
                apellido_m = pedir_texto("el apellido materno")
                contacto = pedir_texto("el contacto")

                registrar_cliente(id_cliente, rut, nombre, apellido_p, apellido_m, contacto)
                print("Cliente registrado.")
                
            if op_clientes == "2":
                listar_clientes()
                
            if op_clientes == "3":
                rut = pedir_texto("el RUT a buscar: ").upper()
                cliente = buscar_cliente(rut)
                
                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print(f"Cliente encontrado: {cliente[2].strip()}"
                          f" {cliente[3].strip()} {cliente[4].strip()}")
                        
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
                pass
            if op_viaje == "2":
                pass
            if op_viaje == "3":
                pass
            if op_viaje == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "5":
        while True:
            print("""
---Opciones Pasajes---
1. Registrar Cliente
2. Listar Cliente
3. Buscar Cliente
4. Volver """)
            
            op_pasajes = input("Ingrese una opcion: ")
            
            if op_pasajes == "1":
                pass
            if op_pasajes == "2":
                pass
            if op_pasajes == "3":
                pass
            if op_pasajes == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "6":
        while True:
            print("""
---Consultas y Reportes---
1. Registrar Cliente
2. Listar Cliente
3. Buscar Cliente
4. Volver """)
            
            op_consulta = input("Ingrese una opcion: ")
            
            if op_consulta == "1":
                pass
            if op_consulta == "2":
                pass
            if op_consulta == "3":
                pass
            if op_consulta == "4":
                print("Opcion Finalizada")
                break
    elif op == "0":
        print("Programa finalizado")
        break
    else:
        print("Opcion Invalida, Ingrese otra nuevamente. ")
            
    