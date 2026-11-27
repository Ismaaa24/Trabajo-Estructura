import os
from config import ARCHIVO_CLIENTES, ENCODE
from algoritmos import busqueda_secuencial, bubble_sort
from persistencia import cargar_clientes


def registrar_cliente(id, rut, nombre, apellido_p, apellido_m, contacto):
    archivo_nuevo = not os.path.exists(ARCHIVO_CLIENTES) or os.path.getsize(ARCHIVO_CLIENTES) == 0
    f = open(ARCHIVO_CLIENTES, "a", encoding=ENCODE)
    if archivo_nuevo:
        f.write("id,rut,nombres,apellido_paterno,apellido_materno,contacto\n")
    f.write(f"{id},{rut},{nombre},{apellido_p},{apellido_m},{contacto}\n")
    f.close()


def lista_De_clientes():
    return cargar_clientes()


def listar_clientes():
    # se ordenan por apellido paterno (columna 3) con bubble sort
    ordenado = bubble_sort(lista_De_clientes(), [3])
    print("ID | RUT | Nombres | Ap. Paterno | Ap. Materno | Contacto")
    for c in ordenado:
        print(c[0], "|", c[1], "|", c[2], "|", c[3], "|", c[4], "|", c[5])


def buscar_cliente(rut):
    return busqueda_secuencial(lista_De_clientes(), 1, rut)


def pedir_id_cliente():
    while True:
        texto = input("Ingrese el ID del cliente: ")
        if texto.isdigit():
            return int(texto)
        print("Ingrese un número entero, por ejemplo 101.")


def pedir_texto(campo):
    while True:
        valor = input(f"Ingrese {campo}: ").strip()
        if valor == "":
            print("Este campo no puede estar vacío.")
        elif "," in valor:
            print("Ingrese el dato sin comas.")
        else:
            return valor
