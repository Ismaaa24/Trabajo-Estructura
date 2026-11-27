# Busqueda secuencial: recorre la lista y devuelve la primera fila
# cuya columna coincide con el valor buscado (o None si no esta).
def busqueda_secuencial(lista, columna, valor):
    valor = str(valor).strip().upper()
    for fila in lista:
        if str(fila[columna]).strip().upper() == valor:
            return fila
    return None


# Arma una lista con los datos de las columnas que se quieren comparar.
# Los textos se pasan a minuscula para ordenar sin importar mayusculas.
def crear_clave(fila, columnas):
    clave = []
    for c in columnas:
        dato = fila[c]
        if isinstance(dato, str):
            dato = dato.strip().lower()
        clave.append(dato)
    return clave


# Bubble sort: compara de a dos y los intercambia si estan al reves.
# "columnas" es la lista de columnas por las que se ordena.
def bubble_sort(lista, columnas):
    copia = lista.copy()
    n = len(copia)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if crear_clave(copia[j], columnas) > crear_clave(copia[j + 1], columnas):
                aux = copia[j]
                copia[j] = copia[j + 1]
                copia[j + 1] = aux
    return copia
