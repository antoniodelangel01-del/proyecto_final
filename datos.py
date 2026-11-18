import json
import os

# Guarda el JSON junto a este archivo, aunque se ejecute desde otra carpeta.
carpeta = os.path.dirname(os.path.abspath(__file__))
archivo_json = os.path.join(carpeta, "estudiantes.json")


def cargar_estudiantes():
    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            estudiantes = json.load(archivo)
    except FileNotFoundError:
        return {}
    if not isinstance(estudiantes, dict):
        raise ValueError("El archivo JSON no tiene el formato esperado.")
    for matricula, estudiante in estudiantes.items():
        if not isinstance(estudiante, dict):
            raise ValueError("Hay un registro incorrecto en el JSON.")
        validar_estudiante(estudiante)
        if matricula != estudiante["id_iest"]:
            raise ValueError("Un ID no coincide con el registro del JSON.")
    return estudiantes


def escribir_estudiantes(estudiantes):
    # Escribe primero una copia temporal para conservar el original si falla.
    archivo_temporal = archivo_json + ".tmp"
    with open(archivo_temporal, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, ensure_ascii=False, indent=4)
    os.replace(archivo_temporal, archivo_json)


def validar_estudiante(estudiante):
    campos = ["nombre", "id_iest", "carrera", "semestre", "correo"]
    for campo in campos:
        if campo not in estudiante:
            raise ValueError(f"Falta el campo: {campo}.")
        if not isinstance(estudiante[campo], str):
            raise ValueError(f"El campo {campo} debe ser texto.")
        if estudiante[campo].strip() == "":
            raise ValueError(f"Completa el campo: {campo}.")
    semestre = estudiante["semestre"]
    try:
        numero = int(semestre)
    except ValueError:
        raise ValueError("El semestre debe ser un número entero.")
    if numero < 1:
        raise ValueError("El semestre debe ser mayor que cero.")
    correo = estudiante["correo"]
    # Comprobación básica; no verifica que la cuenta de correo exista.
    if correo.count("@") != 1 or " " in correo:
        raise ValueError("Revisa el correo, por ejemplo: alumno@iest.edu.mx.")
    usuario, dominio = correo.split("@")
    if usuario == "" or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        raise ValueError("Revisa el correo, por ejemplo: alumno@iest.edu.mx.")


def guardar_estudiante(estudiante):
    validar_estudiante(estudiante)
    estudiantes = cargar_estudiantes()
    matricula = estudiante["id_iest"]
    if matricula in estudiantes:
        raise ValueError("Ese ID ya existe. Utiliza Actualizar.")
    estudiantes[matricula] = estudiante
    escribir_estudiantes(estudiantes)


def buscar_estudiante(matricula):
    estudiantes = cargar_estudiantes()
    if matricula in estudiantes:
        return estudiantes[matricula]
    return None


def actualizar_estudiante(estudiante):
    validar_estudiante(estudiante)
    estudiantes = cargar_estudiantes()
    matricula = estudiante["id_iest"]
    if matricula not in estudiantes:
        raise ValueError("Ese ID no existe. Utiliza Guardar.")
    estudiantes[matricula] = estudiante
    escribir_estudiantes(estudiantes)


def eliminar_estudiante(matricula):
    estudiantes = cargar_estudiantes()
    if matricula not in estudiantes:
        raise ValueError("No existe un estudiante con ese ID.")
    del estudiantes[matricula]
    escribir_estudiantes(estudiantes)


def imprimir_estudiantes(ruta):
    estudiantes = cargar_estudiantes()
    if len(estudiantes) == 0:
        raise ValueError("No hay estudiantes para imprimir.")
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("REGISTRO DE ESTUDIANTES - IEST\n\n")
        for matricula, estudiante in estudiantes.items():
            archivo.write(f"ID IEST: {matricula}\n")
            for campo in ["nombre", "carrera", "semestre", "correo"]:
                archivo.write(f"{campo}: {estudiante[campo]}\n")
            archivo.write("\n")
    return len(estudiantes)
