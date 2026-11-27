def registrar_cliente(id:int,RUT:str,nombre:str,apellidoP:str,apellidoM:str,contacto:str)-> None:
    repo = "clientes.csv"
    encode = "UTF-8"
    f = open(repo,"a",encoding= encode)
    if f.tell() == 0:
        f.write("id,rut,nombres,apellido_paterno,apellido_materno,contacto\n")
    f.write(f"{id},{RUT},{nombre},{apellidoP},{apellidoM},{contacto}\n")
    f.close()

def lista_De_clientes():
    repo = "clientes.csv"
    encode = "UTF-8"
    clientes = [] 
    try:
        f = open(repo,"r",encoding= encode)
    except FileNotFoundError:
        return []
    x = f.readlines()
    f.close()
    for info in x[1:]:
        info = info.strip()
        if info != "":
            clientes.append(info.split(','))
    return clientes

def Bubble_sort(clientes:list) -> list:
    copia = clientes.copy()
    rango = len(copia)
    
    for x in range (rango - 1):
        for z in range (rango - 1 - x):
            if copia[z][3].strip().lower() > copia[z+1][3].strip().lower():
                copia[z], copia[z+1] = copia[z+1], copia[z]
    return copia

def listar_clientes() -> None:
    clientes = lista_De_clientes()
    ordenado = Bubble_sort(clientes)
    print("ID | RUT | Nombres | Ap. Paterno | Ap. Materno | Contacto")
    for c in ordenado:
        print(c[0],"|",c[1],"|",c[2],"|",c[3],"|",c[4],"|",c[5])

def buscar_cliente(rut:str) -> list | None:
    clientes = lista_De_clientes()
    for x in clientes:
        valor = x[1].strip().upper()
        if rut == valor:
            return x
    return None

def pedir_id_cliente() -> int:
    while True:
        try:
            id_cliente = int(input("Ingrese el ID del cliente: "))
            return id_cliente
        except ValueError:
            print("Ingrese un número entero, por ejemplo 101.")


def pedir_texto(campo: str) -> str:
    while True:
        try:
            valor = input(f"Ingrese {campo}: ").strip()

            if valor == "":
                raise ValueError("Este campo no puede estar vacío.")
            if "," in valor:
                raise ValueError("Ingrese el dato sin comas.")

            return valor
        except ValueError as error:
            print(error)