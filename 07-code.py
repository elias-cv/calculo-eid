# Importamos las librerias necesarias para crear 
# la interfaz grafica y graficar la funcion
import customtkinter as ctk # Importamos customtkinter para crear la interfaz grafica
import sympy as sp # Importamos sympy para hacer calculos simbolicos como limites, derivadas, etc.
from matplotlib.figure import Figure # Importamos Figure para graficar la funcion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Importamos FigureCanvasTkAgg para mostrar la grafica en la interfaz grafica
import math # Para usar funciones matematicas como sin, cos, etc.

class Calculadoralimites(ctk.CTk): # Aqui definimos que nuestra aplicacion es una ventana de customTkinter
    def __init__(self): # Funcion que se ejecuta al crear la ventana
        super().__init__() # Para llamar al constructor de la clase padre (CTk)

        self.title("Calculadora de limites UCT") # Configuramos el titulo de la ventana
        self.geometry("1000x500") # Configuramos el tamaño de la ventana (ancho x alto) en pixeles

        # Configura el grid(ubica cosas usando coordenadas) 
        # para que se adapte a cualquier tamaño de ventana
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crea un Frame(caja o contenedor de botones) lateral para los controles (Entradas y Botón)
        self.frame_controles = ctk.CTkFrame(self, width=300)
        self.frame_controles.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 1. Configura la ventana para tener dos columnas
        self.grid_columnconfigure(0, weight=0) # Columna de botones (no crece)
        self.grid_columnconfigure(1, weight=1) # Columna del gráfico (sí crece)

        # 2. Crea el frame donde irá el gráfico (a la derecha)
        self.frame_grafico = ctk.CTkFrame(self)
        self.frame_grafico.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 3. Crea la figura de Matplotlib (el pizarrón)
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figura.add_subplot(111) # El eje donde dibujaremos
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
    
        # Etiqueta para la función f(x)
        self.label_f = ctk.CTkLabel(self.frame_controles, text="Funcion f(x):", font=("Arial", 16))
        self.label_f.pack(pady=(20, 5), padx=10)

        # Entrada para la función f(x)
        self.entrada_f = ctk.CTkEntry(self.frame_controles, placeholder_text="Ej: sen(x)/x o x**2 - 1", width=300)
        self.entrada_f.pack(pady=5, padx=10)

        # Etiqueta para el valor h
        self.label_h = ctk.CTkLabel(self.frame_controles, text="Valor al que tiende (h):", font=("Arial", 16))
        self.label_h.pack(pady=(20, 5), padx=10)

        # Entrada para el valor h
        self.entrada_h = ctk.CTkEntry(self.frame_controles, placeholder_text="Ej: 0, 1, 2, oo", width=300)
        self.entrada_h.pack(pady=5, padx=10)

        # Boton de Calcular
        self.boton_calcular = ctk.CTkButton(self.frame_controles, text="Calcular Limite", command=self.calcular)
        self.boton_calcular.pack(pady= 30, padx= 15)

        # Crea una caja de texto para mostrar el resultado y el procedimiento
        self.resultado_txt = ctk.CTkTextbox(self.frame_controles, width=280, height=150)
        self.resultado_txt.pack(pady=10, padx=10)
        self.resultado_txt.configure(state="disabled")


    def calcular(self):
        try:
            # A. Rescatar los datos
            texto_f = self.entrada_f.get()
            texto_h = self.entrada_h.get()

            x = sp.Symbol('x')
            expresion = sp.sympify(texto_f)
            valor_h = sp.sympify(texto_h)

            # B. Cálculo del límite
            resultado = sp.limit(expresion, x, valor_h)

            # C. PREPARAR EL PASO A PASO (Lógica Analítica)
            pasos = f"PROCEDIMIENTO PASO A PASO:\n"
            pasos += "-" * 30 + "\n"
            pasos += f"Paso 1: Evaluar la función en h = {valor_h}\n"
            
            try:
                # Intentamos evaluar directamente
                evaluacion_directa = expresion.subs(x, valor_h)
                pasos += f"f({valor_h}) = {evaluacion_directa}\n"  
                
                if sustitucion_es_valida(evaluacion_directa):
                    pasos += "Paso 2: Como el valor es definido, el límite es directo.\n"
                    pasos += f"Resultado Final: {resultado}\n"
                elif evaluacion_directa == sp.nan or sp.simplify(evaluacion_directa) == sp.zoo:
                    pasos += "Paso 2: Se detectó una INDETERMINACIÓN (0/0 o similar).\n"
                    pasos += "Paso 3: Intentamos simplificar la expresión...\n"
                    simplificada = sp.simplify(expresion)
                    if simplificada != expresion:
                        pasos += f"Expresión simplificada: {simplificada}\n"
                        pasos += f"Paso 4: Calculamos el límite de la nueva expresión.\n"
                    else:
                        pasos += "Paso 4: Aplicamos Regla de L'Hôpital o identidades.\n"
                    pasos += f"Resultado Final: {resultado}\n"
            except Exception:
                pasos += "Paso 2: Análisis de tendencia (Límite lateral o infinito).\n"
                pasos += f"Resultado Final: {resultado}\n"

            # D. MOSTRAR EN LA INTERFAZ
            self.resultado_txt.configure(state="normal")
            self.resultado_txt.delete("1.0", "end")
            self.resultado_txt.insert("1.0", pasos)
            self.resultado_txt.configure(state="disabled")

            # E. GRÁFICO
            self.ax.clear()
            if valor_h == sp.oo:
                h_num = 10
                puntos_x = [1 + (i * 0.5) for i in range(100)]
            elif valor_h == -sp.oo:
                h_num = -10
                puntos_x = [-50 + (i * 0.5) for i in range(100)]
            else:
                h_num = float(valor_h)
                puntos_x = [h_num - 5 + (i * 0.1) for i in range(101)]
            
            puntos_y = []
            for p in puntos_x:
                try:
                    y_val = float(expresion.subs(x, p))
                    puntos_y.append(y_val)
                except Exception:
                    puntos_y.append(float('nan'))
            
            self.ax.plot(puntos_x, puntos_y, color="blue", label=f"f(x) = {texto_f}")
            if valor_h.is_number and valor_h != sp.oo:
                self.ax.axvline(x=h_num, color='red', linestyle='--', label=f"x = {h_num}")
            
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            self.resultado_txt.configure(state="normal")
            self.resultado_txt.delete("1.0", "end")
            self.resultado_txt.insert("1.0", f"ERROR:\n{e}")
            self.resultado_txt.configure(state="disabled")

# Función auxiliar
def sustitucion_es_valida(val):
    return val.is_number and not val.is_infinite

if __name__ == "__main__":
    app = Calculadoralimites()
    app.mainloop()