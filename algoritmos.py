from typing import Any, Callable, Dict, List, Optional


def busqueda_secuencial(
    registros: List[Dict[str, Any]], clave: str, valor: Any
) -> Optional[Dict[str, Any]]:
    valor_norm: str = str(valor).strip().upper()
    for registro in registros:
        if str(registro.get(clave, "")).strip().upper() == valor_norm:
            return registro
    return None


def bubble_sort(
    datos: List[Dict[str, Any]], clave_comparacion: Callable[[Dict[str, Any]], Any]
) -> List[Dict[str, Any]]:
    copia: List[Dict[str, Any]] = list(datos)
    n: int = len(copia)
    for i in range(n - 1):
        intercambiado: bool = False
        for j in range(0, n - 1 - i):
            if clave_comparacion(copia[j]) > clave_comparacion(copia[j + 1]):
                copia[j], copia[j + 1] = copia[j + 1], copia[j]
                intercambiado = True
        if not intercambiado:
            break
    return copia