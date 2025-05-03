# Guarda este código en un archivo .py y ejecútalo con Python 3
# Requiere: pip install requests beautifulsoup4

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup

class GoogleDorkGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Google Dorks")

        self.operadores_disponibles = [
            ("site:", "Buscar en un sitio web específico"),
            ("inurl:", "Palabra en la URL"),
            ("intitle:", "Palabra en el título"),
            ("intext:", "Palabra en el texto"),
            ("filetype:", "Tipo de archivo xls,doc..."),
            ("ext:", "Extensión de archivo"),
            ("allinurl:", "Todos los términos en la URL"),
            ("allintitle:", "Todos los términos en el título"),
            ("allintext:", "Todos los términos en el texto"),
            ("cache:", "Versión en caché"),
            ("link:", "Enlaces a una página"),
            ("related:", "Páginas similares"),
            ('"..."', "Coincidencia exacta"),
            ("OR", "Búsqueda lógica OR"),
            ("-", "Excluye palabra"),
            ("*", "Comodín")
        ]

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Selecciona los operadores y escribe el texto asociado:").pack(pady=5)
        self.check_vars = []
        self.operador_entries = {}
        self.operador_frames = {}

        frame_operadores = tk.Frame(self.root)
        frame_operadores.pack()

        columnas = 2
        for i, (op, desc) in enumerate(self.operadores_disponibles):
            var = tk.BooleanVar()
            fila = i // columnas
            columna = i % columnas
            op_text = f"{op:<10} ({desc})"
            chk = tk.Checkbutton(frame_operadores, text=op_text, variable=var, anchor="w", justify="left",
                                 command=lambda op=op, var=var: self.toggle_operador_entry(op, var))
            chk.grid(row=fila, column=columna, sticky="w", padx=10, pady=2)
            self.check_vars.append((op, var))

            operador_frame = tk.Frame(frame_operadores)
            operador_frame.grid(row=fila, column=columna, padx=10, pady=2)
            operador_label = tk.Label(operador_frame, text=op, anchor="w")
            operador_label.grid(row=0, column=0, sticky="w")

            entry = tk.Entry(operador_frame, width=50)
            entry.grid(row=1, column=0, padx=10, pady=2)
            entry.grid_remove()
            self.operador_entries[op] = entry
            self.operador_frames[op] = operador_frame

        boton_frame = tk.Frame(self.root)
        boton_frame.pack(pady=10)

        tk.Button(boton_frame, text="Generar Dorks", command=self.generar_dorks).pack(side="left", padx=5)
        tk.Button(boton_frame, text="Guardar en archivo", command=self.guardar_dorks).pack(side="left", padx=5)
        tk.Button(boton_frame, text="Ver ejemplos útiles", command=self.mostrar_ayuda).pack(side="left", padx=5)
        tk.Button(boton_frame, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)

        self.resultado_texto = tk.Text(self.root, wrap="word", height=5, width=80)
        self.resultado_texto.pack(pady=10)
        self.resultado_texto.config(state=tk.DISABLED)

        self.boton_copiar = tk.Button(self.root, text="Copiar Dork al portapapeles", command=self.copiar_dork)
        self.boton_copiar.pack(pady=5)

        self.boton_google = tk.Button(self.root, text="Buscar en Google", command=self.buscar_en_google)
        self.boton_google.pack(pady=5)

        tk.Label(self.root, text="Resultados encontrados en Google (solo títulos):").pack()
        self.google_results_text = tk.Text(self.root, wrap="word", height=15, width=80)
        self.google_results_text.pack(pady=10)
        self.google_results_text.config(state=tk.DISABLED)

    def toggle_operador_entry(self, operador, var):
        entry = self.operador_entries[operador]
        if var.get():
            entry.grid()
        else:
            entry.grid_remove()

    def generar_dorks(self):
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.google_results_text.config(state=tk.NORMAL)
        self.google_results_text.delete(1.0, tk.END)
        self.google_results_text.config(state=tk.DISABLED)

        operadores_con_entradas = []
        for op, var in self.check_vars:
            if var.get():
                valor = self.operador_entries[op].get().strip()
                if valor:
                    operadores_con_entradas.append((op, valor))

        if not operadores_con_entradas:
            messagebox.showerror("Error", "Debes seleccionar al menos un operador y escribir un valor asociado.")
            return

        dork = " ".join([f'{op}{valor}' for op, valor in operadores_con_entradas])
        self.resultado_texto.insert(tk.END, dork + "\n")
        self.resultado_texto.config(state=tk.DISABLED)
        messagebox.showinfo("Listo", f"Dork generada con {len(operadores_con_entradas)} operadores.")

    def copiar_dork(self):
        dork = self.resultado_texto.get(1.0, tk.END).strip()
        if dork:
            self.root.clipboard_clear()
            self.root.clipboard_append(dork)
            self.root.update()
            messagebox.showinfo("Copiado", "Dork copiado al portapapeles.")
        else:
            messagebox.showwarning("Advertencia", "No hay Dork generado para copiar.")

    def buscar_en_google(self):
        dork = self.resultado_texto.get(1.0, tk.END).strip()
        if not dork:
            messagebox.showwarning("Advertencia", "No hay Dork generado para buscar.")
            return

        query = urllib.parse.quote_plus(dork)
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("h3")
            self.google_results_text.config(state=tk.NORMAL)
            self.google_results_text.delete(1.0, tk.END)
            for result in results[:10]:
                if result.text.strip():
                    self.google_results_text.insert(tk.END, f"- {result.text.strip()}\n\n")
            self.google_results_text.config(state=tk.DISABLED)
        except Exception as e:
            self.google_results_text.config(state=tk.NORMAL)
            self.google_results_text.insert(tk.END, f"[!] No se pudieron obtener resultados: {e}\n")
            self.google_results_text.config(state=tk.DISABLED)

    def guardar_dorks(self):
        contenido = self.resultado_texto.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay dorks generadas para guardar.")
            return

        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if archivo:
            with open(archivo, "w") as f:
                f.write(contenido)
            messagebox.showinfo("Guardado", f"Dorks guardadas en {archivo}")

    def limpiar_campos(self):
        self.resultado_texto.config(state=tk.NORMAL)
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.config(state=tk.DISABLED)
        self.google_results_text.config(state=tk.NORMAL)
        self.google_results_text.delete(1.0, tk.END)
        self.google_results_text.config(state=tk.DISABLED)
        for op, var in self.check_vars:
            var.set(False)
        for entry in self.operador_entries.values():
            entry.delete(0, tk.END)
            entry.grid_remove()
        messagebox.showinfo("Limpiado", "Se han limpiado todos los campos y resultados.")

    def mostrar_ayuda(self):
        ayuda = Toplevel(self.root)
        ayuda.title("Ejemplos útiles de Google Dorks")
        ayuda.geometry("700x500")
        texto = tk.Text(ayuda, wrap="word")
        texto.pack(expand=True, fill="both")

        contenido = """
Ejemplos útiles de Google Dorks

site:gov filetype:xls inurl:"contacts"
"index of" admin
intitle:"index of /" password
filetype:log intext:password
inurl:wp-content/uploads
site:edu login

Estos dorks permiten encontrar archivos expuestos, accesos administrativos y documentos sensibles públicos. Puedes adaptarlos a tus necesidades de auditoría u OSINT.
        """

        texto.insert(tk.END, contenido)
        texto.config(state=tk.DISABLED)

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleDorkGeneratorApp(root)
    root.mainloop()
