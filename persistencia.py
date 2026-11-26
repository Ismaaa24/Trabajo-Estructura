import os
from typing import Any, Dict, List
from config import (
    ARCHIVO_BUSES,
    ARCHIVO_CIUDADES,
    ARCHIVO_CLIENTES,
    ARCHIVO_PASAJES,
    ARCHIVO_VIAJES,
    ENCODE,
)

CIUDADES_POR_DEFECTO: List[Dict[str, str]] = [
    {"id_ciudad": "1", "nombre": "Concepción", "posicion": "0"},
    {"id_ciudad": "2", "nombre": "Chillán", "posicion": "1"},
    {"id_ciudad": "3", "nombre": "Linares", "posicion": "2"},
    {"id_ciudad": "4", "nombre": "Talca", "posicion": "3"},
    {"id_ciudad": "5", "nombre": "Rancagua", "posicion": "4"},
    {"id_ciudad": "6", "nombre": "Santiago", "posicion": "5"},
]


def cargar_ciudades_csv() -> List[Dict[str, Any]]:
    ciudades: List[Dict[str, Any]] = []
    if os.path.exists(ARCHIVO_CIUDADES) and os.path.getsize(ARCHIVO_CIUDADES) > 0:
        try:
            with open(ARCHIVO_CIUDADES, "r", encoding=ENCODE) as f:
                lineas: List[str] = f.readlines()
            for linea in lineas[1:]:
                linea_limpia: str = linea.strip()
                if not linea_limpia:
                    continue
                partes: List[str] = [p.strip() for p in linea_limpia.split(",")]
                if len(partes) >= 3:
                    ciudades.append(
                        {
                            "id_ciudad": partes[0],
                            "nombre": partes[1],
                            "posicion": int(partes[2]),
                        }
                    )
        except (OSError, ValueError):
            ciudades = []

    if not ciudades:
        for c in CIUDADES_POR_DEFECTO:
            ciudades.append(
                {
                    "id_ciudad": c["id_ciudad"],
                    "nombre": c["nombre"],
                    "posicion": int(c["posicion"]),
                }
            )
    return ciudades


def cargar_buses_csv() -> List[Dict[str, Any]]:
    buses: List[Dict[str, Any]] = []
    if not os.path.exists(ARCHIVO_BUSES):
        return buses
    try:
        with open(ARCHIVO_BUSES, "r", encoding=ENCODE) as f:
            lineas: List[str] = f.readlines()
        for linea in lineas[1:]:
            linea_limpia: str = linea.strip()
            if not linea_limpia:
                continue
            partes: List[str] = [p.strip() for p in linea_limpia.split(",")]
            if len(partes) >= 4:
                buses.append(
                    {
                        "id_bus": partes[0],
                        "patente": partes[1].lstrip("+"),
                        "capacidad": int(partes[2]),
                        "estado": partes[3],
                    }
                )
    except (OSError, ValueError):
        return []
    return buses


def cargar_clientes_csv() -> List[Dict[str, str]]:
    clientes: List[Dict[str, str]] = []
    rutas_posibles: List[str] = [
        ARCHIVO_CLIENTES,
        "repositorio clientes.csv",
        "repositorio.csv",
    ]
    for ruta in rutas_posibles:
        if not os.path.exists(ruta):
            continue
        try:
            with open(ruta, "r", encoding=ENCODE) as f:
                lineas: List[str] = f.readlines()
            for linea in lineas[1:]:
                linea_limpia: str = linea.strip()
                if not linea_limpia:
                    continue
                partes: List[str] = [p.strip() for p in linea_limpia.split(",")]
                if len(partes) >= 6:
                    if partes[0].startswith("ID:"):
                        id_cli = partes[0].split(":", 1)[1].strip()
                        nom = partes[1].split(":", 1)[1].strip()
                        ap_p = partes[2].split(":", 1)[1].strip()
                        ap_m = partes[3].split(":", 1)[1].strip()
                        rut = partes[4].split(":", 1)[1].strip()
                        cont = partes[5].split(":", 1)[1].strip()
                    else:
                        id_cli, rut, nom, ap_p, ap_m, cont = partes[:6]
                    clientes.append(
                        {
                            "id_cliente": id_cli,
                            "rut": rut,
                            "nombres": nom,
                            "apellido_paterno": ap_p,
                            "apellido_materno": ap_m,
                            "contacto": cont,
                        }
                    )
        except (OSError, IndexError):
            continue
    return clientes


def cargar_viajes_csv() -> List[Dict[str, Any]]:
    viajes: List[Dict[str, Any]] = []
    if not os.path.exists(ARCHIVO_VIAJES):
        return viajes
    try:
        with open(ARCHIVO_VIAJES, "r", encoding=ENCODE) as f:
            lineas: List[str] = f.readlines()
        for linea in lineas[1:]:
            linea_limpia: str = linea.strip()
            if not linea_limpia:
                continue
            partes: List[str] = [p.strip() for p in linea_limpia.split(",")]
            if len(partes) >= 7:
                viajes.append(
                    {
                        "id_viaje": partes[0],
                        "id_bus": partes[1],
                        "fecha": partes[2],
                        "hora": partes[3],
                        "id_origen": partes[4],
                        "id_destino": partes[5],
                        "tarifa_base": int(partes[6]),
                    }
                )
    except (OSError, ValueError):
        return []
    return viajes


def cargar_pasajes_csv() -> List[Dict[str, Any]]:
    pasajes: List[Dict[str, Any]] = []
    if not os.path.exists(ARCHIVO_PASAJES):
        return pasajes
    try:
        with open(ARCHIVO_PASAJES, "r", encoding=ENCODE) as f:
            lineas: List[str] = f.readlines()
        for linea in lineas[1:]:
            linea_limpia: str = linea.strip()
            if not linea_limpia:
                continue
            partes: List[str] = [p.strip() for p in linea_limpia.split(",")]
            if len(partes) >= 8:
                pasajes.append(
                    {
                        "id_pasaje": partes[0],
                        "id_viaje": partes[1],
                        "id_cliente": partes[2],
                        "id_origen": partes[3],
                        "id_destino": partes[4],
                        "asiento": int(partes[5]),
                        "valor": int(partes[6]),
                        "estado": partes[7],
                    }
                )
    except (OSError, ValueError):
        return []
    return pasajes