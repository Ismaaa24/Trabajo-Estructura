from os import system
from clientes import registrar_cliente,lista_De_clientes,Bubble_sort,listar_clientes,buscar_cliente
id = 100
from config import ARCHIVO_BUSES, ARCHIVO_CIUDADES, ENCODE
from funciones_buses import listar_buses, registrar_buses

while True:
    system("cls")
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
                while True:
                    try:
                        rut = input("Ingrese su RUT -> ")
                        if rut == "":
                            raise Exception("Por favor complete el campo solicitado...")
                        respuesta = buscar_cliente(rut)
                        if respuesta is not None:
                            print("Cliente ya registrado...")
                            break
                        nombre = input("Ingrese su nombre -> ").capitalize()
                        if nombre == "":
                            raise Exception("Por favor complete el campo solicitado...")
                        apellidoP = input("Ingrese su apellido paterno -> ").capitalize()
                        if apellidoP == "":
                            raise Exception("Por favor complete el campo solicitado...")
                        apellidoM = input("Ingrese su apellido materno -> ").capitalize()
                        if apellidoM == "":
                            raise Exception("Por favor complete el campo solicitado...")
                        contacto = input("Ingrese su contacto de preferencia -> ")
                        if contacto == "":
                            raise Exception("Por favor complete el campo solicitado...")
                        id += 1
                        registrar_cliente(id,rut,nombre,apellidoP,apellidoM,contacto)
                        input("Cliente registrado con exito, presione cualquier tecla para continuar...")
                        break
                    except Exception as err:
                        print(err)
            if op_clientes == "2":
                listar_clientes()
            if op_clientes == "3":
                
                buscar = input("Ingrese el rut del cliente a buscar ->")
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
                pass
            if op_buses == "4":
                print("Opcion Finalizada")
                break
            
    elif op == "3":
        pass
    
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
            
    