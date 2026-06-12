import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class CalculadoraLimites(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de límites UCT")
        self.geometry("1100x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_portada = self.tabs.add("INICIO")
        self.tab_Calculadora_limites = self.tabs.add("Calculadora de Límites")

        self.crear_portada()
        self.crear_calculadora_limites()

    def crear_portada(self):
        titulo = ctk.CTkLabel(
            self.tab_portada,
            text="Calculadora de Límites UCT",
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=30)

        texto = """
Plataforma Tecnologica de apoyo academico interactiva, diseñada para calcular límites(algebraicos, infinitos, 
al infinito y trigonométricos) y visualizar asíntotas.
Desarrollada por 3 GENIOS(Ingenieros Vikingos, 24/7, Hasta las 3 DE la mañana), estudiantes de la carrera Ingenieria Informatica.

¡¡¡REGLAS IMPLEMENTADAS!!!:

Para usar esta Calculadora.

1. Escribir el límite en la forma f(x) y el valor al que tiende x (h).

2. ¡¡OJ0!!: Para infinito usar "oo" o "inf", para pi usar "pi" o "π".

3. Para calcular Limites con raices, valor absoluto o funciones trigonometricas.
    usar la sintaxis de sympy:

     RAIZ(√(x)) = sympy (sqrt(x))

     VALOR ABSOLUTO(|x|) = sympy (Abs(x))

     SENO(sen(x)) = sympy (sin(x))

     COSENO(cos(x)) = sympy (cos(x))

     TANGENTE(tan(x)) = sympy (tan(x))
"""
        caja = ctk.CTkTextbox(self.tab_portada, width=800, height=350, font=("Arial", 12))
        caja.pack(pady=20)
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    def crear_calculadora_limites(self):
        contenedor = ctk.CTkFrame(self.tab_Calculadora_limites)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel de controles
        panel = ctk.CTkFrame(contenedor, width=380)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico_frame = ctk.CTkFrame(contenedor)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Control de Cálculo", font=("Arial", 20, "bold")).pack(pady=10)

        ctk.CTkLabel(panel, text="Función f(x):").pack()
        self.f_x = ctk.CTkEntry(panel, placeholder_text="Ej: (x**2-1)/(x-1)", width=250)
        self.f_x.pack(pady=5)

        ctk.CTkLabel(panel, text="Valor h (tiende a):").pack()
        self.tiende_h = ctk.CTkEntry(panel, placeholder_text="Ej: 1, pi o oo", width=250)
        self.tiende_h.pack(pady=5)

        ctk.CTkButton(panel, text="Calcular y Graficar", command=self.ejecutar_calculo).pack(pady=20)

        self.resultado_txt = ctk.CTkTextbox(panel, width=340, height=300)
        self.resultado_txt.pack(pady=10, padx=10)

        self.figura, self.eje, self.canvas = self.crear_canvas(grafico_frame)

    def limpiar_y_escribir(self, texto):
        self.resultado_txt.configure(state="normal")
        self.resultado_txt.delete("1.0", "end")
        self.resultado_txt.insert("end", texto)
        self.resultado_txt.configure(state="disabled")

    def ejecutar_calculo(self):
        """Función puente para manejar el flujo"""
        enunciado_f = self.f_x.get()
        valor_h_str = self.tiende_h.get()
        
        try:
            x = sp.Symbol('x')
            f = sp.sympify(enunciado_f)
            
            # Procesar h
            h_str = valor_h_str.lower().strip()
            if h_str in ["oo", "inf"]: h = sp.oo
            elif h_str in ["-oo", "-inf"]: h = -sp.oo
            else: h = sp.sympify(h_str.replace("π", "pi"))

            pasos, res_final = self.calcular_limites_logica(f, h, x)
            asintotas_info = self.analizar_asintotas(f, x)
            
            # Mostrar todo en el cuadro de texto
            info_completa = pasos + "\n" + "-"*30 + "\n" + asintotas_info
            self.limpiar_y_escribir(info_completa)
            
            # Graficar
            self.graficar(f, h, x)

        except Exception as e:
            self.limpiar_y_escribir(f"Error: {e}")

    def calcular_limites_logica(self, f, h, x):
        """Lógica paso a paso sin usar sympy.limit() directo."""
        pasos = [f"--- ANÁLISIS DE LÍMITE ---\nx tiende a: {h}\n"]
        
        # 1. Valor Absoluto
        if f.has(sp.Abs) and h.is_finite:
            pasos.append("Paso: Análisis lateral por Valor Absoluto...\n")
            izq = f.subs(x, float(h) - 0.0001).evalf(4)
            der = f.subs(x, float(h) + 0.0001).evalf(4)
            if abs(izq - der) > 0.1:
                return "".join(pasos) + f"Límites laterales: {izq} != {der}\nResultado: NO EXISTE", None

        # 2. Evaluación directa
        try:
            res = f.subs(x, h)
            if res.is_finite and not res.has(sp.nan):
                pasos.append(f"Paso 1: Evaluación directa exitosa.\nResultado = {res}")
                return "".join(pasos), res
        except: pass

        # 3. Simplificación
        f_can = sp.cancel(f)
        if f_can != f:
            pasos.append(f"Paso 2: Simplificación detectada.\nNueva f(x): {f_can}\n")
            res = f_can.subs(x, h)
            if res.is_finite: return "".join(pasos) + f"Resultado = {res}", res

# --- NUEVA ESTRATEGIA: CONVERGENCIA NUMÉRICA (TABLA DE VALORES) ---
        # Reemplazamos L'Hôpital por la técnica de la Guía 6: acercarse a h
        if not res.is_finite or res.has(sp.nan):
            pasos.append("Paso 3: Indeterminación detectada. Aplicando Método de Aproximación Numérica (Tabla de Valores)...\n")
            
            # Solo si h es un número finito
            if h.is_finite:
                pasos.append(f"{'Dirección':<12} | {'x':<12} | {'f(x)':<12}\n")
                pasos.append("-" * 40 + "\n")
                
                epsilon = [0.1, 0.01, 0.001, 0.0001]
                v_izq, v_der = 0, 0
                
                for e in epsilon:
                    # Calculamos valores muy cercanos a h
                    x_izq = float(h) - e
                    x_der = float(h) + e
                    
                    try:
                        f_izq = float(f.subs(x, x_izq).evalf())
                        f_der = float(f.subs(x, x_der).evalf())
                        
                        pasos.append(f"{'Izquierda':<12} | {x_izq:<12.4f} | {f_izq:<12.6f}\n")
                        pasos.append(f"{'Derecha':<12} | {x_der:<12.4f} | {f_der:<12.6f}\n")
                        
                        v_izq, v_der = f_izq, f_der
                    except:
                        continue
                
                # Si los valores por ambos lados convergen (son casi iguales)
                if abs(v_izq - v_der) < 0.001:
                    resultado_aprox = round(v_izq, 2)
                    pasos.append(f"\nConclusión: f(x) converge a {resultado_aprox} por ambos lados.\n")
                    return "".join(pasos), resultado_aprox
                else:
                    pasos.append("\nConclusión: Los valores no convergen. El límite podría no existir o ser infinito.\n")
                    return "".join(pasos), sp.oo

    def analizar_asintotas(self, f, x):
        info = "--- ANÁLISIS DE ASÍNTOTAS ---\n"
        num, den = sp.fraction(f)
        
        # Asíntotas Verticales (Raíces del denominador)
        try:
            raices = sp.solve(den, x)
            if raices:
                info += f"A. Verticales en x = {raices}\n"
            else:
                info += "No se detectaron A. Verticales.\n"
        except: info += "Error buscando A. Verticales.\n"

        # Asíntotas Horizontales (Límite al infinito)
        try:
            # Aquí usamos el análisis de grados para cumplir la lógica
            deg_num = sp.degree(num, x) if hasattr(num, 'as_poly') else 0
            deg_den = sp.degree(den, x) if hasattr(den, 'as_poly') else 0
            
            if deg_num < deg_den:
                info += "A. Horizontal en y = 0\n"
            elif deg_num == deg_den:
                # Cociente de coeficientes principales
                lc_num = sp.Poly(num, x).LC()
                lc_den = sp.Poly(den, x).LC()
                info += f"A. Horizontal en y = {lc_num/lc_den}\n"
            else:
                info += "No tiene A. Horizontal (crece al infinito).\n"
        except: info += "Análisis de A. Horizontal no aplicable.\n"
        
        return info

    def graficar(self, f, h_val, x_sym):
        self.eje.clear()
        
        # Rango de gráfico (SIN NUMPY)
        try: centro = float(h_val) if h_val.is_finite else 0
        except: centro = 0
        
        puntos_x = []
        puntos_y = []
        inicio = centro - 10
        paso = 0.1 # Rúbrica: Ciclo manual
        
        for i in range(200):
            vx = inicio + (i * paso)
            try:
                vy = float(f.subs(x_sym, vx).evalf())
                if -50 < vy < 50: # Evitar que el gráfico se dispare
                    puntos_x.append(vx)
                    puntos_y.append(vy)
                else:
                    puntos_x.append(vx); puntos_y.append(None)
            except: 
                puntos_x.append(vx); puntos_y.append(None)

        self.eje.plot(puntos_x, puntos_y, label="f(x)", color="#1f77b4")
        
        # Graficar Asíntotas Verticales
        num, den = sp.fraction(f)
        try:
            for r in sp.solve(den, x_sym):
                if r.is_real:
                    self.eje.axvline(x=float(r), color='red', linestyle=':', label='A.V.')
        except: pass

        if h_val.is_finite:
            self.eje.scatter([float(h_val)], [0], color='orange', zorder=5, label=f"Tendencia x={h_val}")

        self.eje.axhline(0, color='black', lw=1)
        self.eje.axvline(0, color='black', lw=1)
        self.eje.legend(fontsize='small')
        self.eje.grid(True, alpha=0.3)
        self.canvas.draw()

if __name__ == "__main__":
    app = CalculadoraLimites()
    app.mainloop()