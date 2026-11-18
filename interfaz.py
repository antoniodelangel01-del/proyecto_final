import tkinter as tk
from tkinter import messagebox, filedialog
import datos


def obtener_datos():
    estudiante = {
        "nombre": entrada_nombre.get().strip(),
        "id_iest": entrada_id_iest.get().strip(),
        "carrera": entrada_carrera.get().strip(),
        "semestre": entrada_semestre.get().strip(),
        "correo": entrada_correo.get().strip(),
    }
    return estudiante


def obtener_id():
    matricula = entrada_id_iest.get().strip()
    if matricula == "":
        raise ValueError("Escribe el ID IEST.")
    return matricula


def guardar():
    try:
        estudiante = obtener_datos()
        datos.guardar_estudiante(estudiante)
        messagebox.showinfo("Guardar", "Estudiante guardado.")
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo guardar", str(error))


def buscar():
    try:
        matricula = obtener_id()
        estudiante = datos.buscar_estudiante(matricula)
        if estudiante is None:
            limpiar()
            entrada_id_iest.insert(0, matricula)
            messagebox.showinfo("Buscar", "No se encontró ese ID.")
            return
        limpiar()
        entrada_nombre.insert(0, estudiante["nombre"])
        entrada_id_iest.insert(0, estudiante["id_iest"])
        entrada_carrera.insert(0, estudiante["carrera"])
        entrada_semestre.insert(0, estudiante["semestre"])
        entrada_correo.insert(0, estudiante["correo"])
        messagebox.showinfo("Buscar", "Estudiante encontrado.")
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo buscar", str(error))


def actualizar():
    try:
        estudiante = obtener_datos()
        datos.validar_estudiante(estudiante)
        if messagebox.askyesno("Actualizar", "¿Reemplazar los datos de este ID?"):
            datos.actualizar_estudiante(estudiante)
            messagebox.showinfo("Actualizar", "Estudiante actualizado.")
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo actualizar", str(error))


def eliminar():
    try:
        matricula = obtener_id()
        estudiante = datos.buscar_estudiante(matricula)
        if estudiante is None:
            messagebox.showerror("Eliminar", "No existe un estudiante con ese ID.")
            return
        nombre = estudiante["nombre"]
        if messagebox.askyesno("Eliminar", f"¿Eliminar a {nombre}, ID {matricula}?"):
            datos.eliminar_estudiante(matricula)
            limpiar()
            messagebox.showinfo("Eliminar", "Estudiante eliminado.")
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo eliminar", str(error))


def imprimir():
    ruta = filedialog.asksaveasfilename(
        title="Guardar lista de estudiantes",
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt")],
        initialfile="lista_estudiantes.txt")
    if ruta == "":
        return
    try:
        cantidad = datos.imprimir_estudiantes(ruta)
        messagebox.showinfo("Imprimir", f"Se guardaron {cantidad} estudiantes en:\n{ruta}")
    except (ValueError, OSError) as error:
        messagebox.showerror("No se pudo imprimir", str(error))


def limpiar():
    entrada_nombre.delete(0, tk.END)
    entrada_id_iest.delete(0, tk.END)
    entrada_carrera.delete(0, tk.END)
    entrada_semestre.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)


# Ventana y colores: naranja aproximado, inspirado en el IEST.
naranja = "#F47721"
blanco = "#FFFFFF"
texto = "#252525"
ventana = tk.Tk()
ventana.title("Registro de estudiantes - IEST")
ventana.config(bg=naranja)
ventana.minsize(600, 530)

titulo = tk.Label(ventana, text="IEST ANÁHUAC", bg=naranja,
                  fg=blanco, font=("Arial", 22, "bold"))
titulo.pack(pady=(20, 4))
subtitulo = tk.Label(ventana, text="Registro de estudiantes", bg=naranja,
                     fg=texto, font=("Arial", 14))
subtitulo.pack(pady=(0, 14))

formulario = tk.Frame(ventana, bg=blanco, padx=24, pady=16)
formulario.pack(padx=24, fill="x")
formulario.columnconfigure(1, weight=1)

etiqueta_nombre = tk.Label(formulario, text="Nombre:", bg=blanco, fg=texto)
etiqueta_nombre.grid(row=0, column=0, sticky="w", pady=8)
entrada_nombre = tk.Entry(formulario, width=38, font=("Arial", 11))
entrada_nombre.grid(row=0, column=1, sticky="ew", padx=(14, 0), pady=8)

etiqueta_id_iest = tk.Label(formulario, text="ID IEST:", bg=blanco, fg=texto)
etiqueta_id_iest.grid(row=1, column=0, sticky="w", pady=8)
entrada_id_iest = tk.Entry(formulario, width=38, font=("Arial", 11))
entrada_id_iest.grid(row=1, column=1, sticky="ew", padx=(14, 0), pady=8)

etiqueta_carrera = tk.Label(formulario, text="Carrera:", bg=blanco, fg=texto)
etiqueta_carrera.grid(row=2, column=0, sticky="w", pady=8)
entrada_carrera = tk.Entry(formulario, width=38, font=("Arial", 11))
entrada_carrera.grid(row=2, column=1, sticky="ew", padx=(14, 0), pady=8)

etiqueta_semestre = tk.Label(formulario, text="Semestre:", bg=blanco, fg=texto)
etiqueta_semestre.grid(row=3, column=0, sticky="w", pady=8)
entrada_semestre = tk.Entry(formulario, width=38, font=("Arial", 11))
entrada_semestre.grid(row=3, column=1, sticky="ew", padx=(14, 0), pady=8)

etiqueta_correo = tk.Label(formulario, text="Correo:", bg=blanco, fg=texto)
etiqueta_correo.grid(row=4, column=0, sticky="w", pady=8)
entrada_correo = tk.Entry(formulario, width=38, font=("Arial", 11))
entrada_correo.grid(row=4, column=1, sticky="ew", padx=(14, 0), pady=8)

# Los botones quedan sobre una zona naranja.
botones = tk.Frame(ventana, bg=naranja)
botones.pack(pady=16)

boton_guardar = tk.Button(botones, text="Guardar", command=guardar,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_guardar.grid(row=0, column=0, padx=5, pady=5)

boton_buscar = tk.Button(botones, text="Buscar", command=buscar,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_buscar.grid(row=0, column=1, padx=5, pady=5)

boton_actualizar = tk.Button(botones, text="Actualizar", command=actualizar,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_actualizar.grid(row=0, column=2, padx=5, pady=5)

boton_eliminar = tk.Button(botones, text="Eliminar", command=eliminar,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_eliminar.grid(row=1, column=0, padx=5, pady=5)

boton_imprimir = tk.Button(botones, text="Imprimir", command=imprimir,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_imprimir.grid(row=1, column=1, padx=5, pady=5)

boton_limpiar = tk.Button(botones, text="Limpiar", command=limpiar,
                           width=13, bg=blanco, fg=texto,
                           activebackground="#FFE1C8", font=("Arial", 10))
boton_limpiar.grid(row=1, column=2, padx=5, pady=5)

aviso = tk.Label(ventana, text="Para buscar o eliminar, escribe el ID IEST.",
                 bg=naranja, fg=texto)
aviso.pack(pady=(0, 18))
