def registrar_cliente(id:int,RUT:str,nombre:str,apellidoP:str,apellidoM:str,contacto:str)-> None:
    repo = "repositorio clientes.csv"
    encode = "UTF-8"
    f = open(repo,"a",encoding= encode)
    f.write(f"ID: {id}, Nombre: {nombre}, Apellido Paterno: {apellidoP}, Apellido Materno: {apellidoM}, RUT: {RUT}, Contacto: {contacto}\n")
    f.close

def lista_De_clientes():
    repo = "repositorio clientes.csv"
    encode = "UTF-8"
    clientes = [] 
    f = open(repo,"r",encoding= encode)
    x = f.readlines()
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
            if copia[z][3].lower() > copia[z+1][3].lower():
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
        valor = x[4].split(":", 1)[1].strip()
        if rut == valor:
            return x
        
    return None