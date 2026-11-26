from config import ARCHIVO_BUSES, ENCODE

def listar_buses() -> None:
    f = open(ARCHIVO_BUSES, "r", encoding = ENCODE)
    lista = f.readlines()
    f.close()
    print(f"{'ID BUS':<10} {'PATENTE':<10} {'CAPACIDAD':<10} ESTADO")
                
    for registro in lista[1:]:
        if registro.strip() == "":
            continue 
        
        id_bus, patente, capacidad, estado = registro.strip().split(",")
        print(f"{id_bus.strip():<10} {patente.strip():<10} {capacidad.strip():>5} {estado.strip():>10}")

def registrar_buses() -> None: 
    while True:
        try:
            id_bus = input("Ingrese el ID del bus: ").strip().upper()
            if id_bus == "":
                raise ValueError("El ID del bus no puede estar vacio. ")
            if not id_bus.startswith("BUS_") or not id_bus[4:].isdigit():
                raise ValueError("Use el Formato BUS_ Seguido de numeros, por ejemplo BUS_01")
            break
        except ValueError as error:
            print(error)
    while True:
        try:
            patente = input("Ingrese la patente del bus: ").strip().upper()
            if patente == "":
                raise ValueError("La patente no puede estar vacia. ")
            if len(patente) != 6 or patente[3] != "-":
                raise ValueError("Use el formato de patente ABC-12")
            if not patente[:3].isalpha() or not patente[4:].isdigit():
                raise ValueError("Ingrese tres letras, un guion y dos numeros. ")
            break
        except ValueError as error:
            print(error)
    while True:
        try:            
            capacidad = int(input("Ingrese la capacidad del bus: "))
        except ValueError:
            print("Ingrese un numero entero, por ejemplo 30. ")
            continue
        if capacidad <= 0:
            print("La capacidad debe ser mayor que 0. ")
            continue
        break
    while True:
        try:
            estado = input("Ingrese el estado del bus (DISPONIBLE / NO DISPONIBLE): ").strip().upper()
            if estado not in ("DISPONIBLE", "NO DISPONIBLE"):
                raise ValueError("El estado debe ser DISPONIBLE o NO DISPONIBLE")
            break
        except ValueError as error:
            print(error)
        
    f = open(ARCHIVO_BUSES, "r", encoding=ENCODE)
    lista = f.readlines()
    f.close()
    
    for registro in lista[1:]:
        if registro.strip() == "":
            continue 
           
        datos = registro.strip().split(",")
        id_guardado = datos[0].strip().upper()
        patente_guardada = datos[1].strip().upper()
        
        if id_guardado == id_bus:
            print("Ya existe un bus con esa ID. ")
            return
        elif patente_guardada == patente:
            print("Ya existe un bus con esa patente. ")
            return

    f = open(ARCHIVO_BUSES, "a", encoding=ENCODE)
    if not lista:
        f.write("id_bus,patente,capacidad,estado\n")
    f.write(f"{id_bus},+{patente},{capacidad},{estado}\n")
    f.close()
    print("Bus registrado exitosamente!")

def anular_pasaje():
    pass
