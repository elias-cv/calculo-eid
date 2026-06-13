import customtkinter as ctk # Biblioteca para crear la interfaz gráfica.
from matplotlib.figure import Figure # Para crear la figura donde irá el gráfico.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Para integrar el gráfico de matplotlib en Tkinter.
import sympy as sp  # Biblioteca de matemáticas simbólicas (para resolver límites, ecuaciones, etc.)
import re # Biblioteca para usar expresiones regulares (búsqueda y reemplazo de texto complejo).

# -- CLASE PRINCIPAL DE LA APLICACIÓN --
class CalculadoraLimites(ctk.CTk):
    def __init__(self):
        super().__init__() # Inicializa la ventana principal de CustomTkinter.

        # Configuración básica de la ventana
        self.title("Calculadora de límites UCT") # Titulo
        self.geometry("1100x700") # Tamaño de la ventana: Ancho x Alto

        # Configuración visual (Modo oscuro y azules)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuración del sistema de cuadrícula para que los elementos se expandan al redimensionar (se adaptan a la pantalla)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Creación del sistema de pestañas
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Añadimos dos pestañas: INICIO (Portada) y la Calculadora
        self.tab_portada = self.tabs.add("INICIO")
        self.tab_Calculadora_limites = self.tabs.add("Calculadora de Límites")

        # Llamamos a los métodos que construyen el contenido de cada pestaña
        self.crear_portada()
        self.crear_calculadora_limites()

    # --- CREACIÓN DE LA PORTADA ---
    def crear_portada(self):

        # Título principal
        titulo = ctk.CTkLabel(
            self.tab_portada,
            text="Calculadora de Límites UCT", 
            font=("Arial", 28, "bold")
        )
        titulo.pack(pady=30)
        # Instrucciones de uso de la calculadora
        texto = """
Plataforma Tecnologica de apoyo academico interactiva, diseñada para calcular límites(algebraicos, infinitos, 
al infinito y trigonométricos) y visualizar asíntotas.
Desarrollada por 3 GENIOS(Ingenieros Vikingos, 24/7, Hasta las 3 DE la mañana), estudiantes de la carrera Ingenieria Informatica.

¡¡¡REGLAS IMPLEMENTADAS!!!:

Para usar esta Calculadora.

1. Escribir el límite en la forma f(x) y el valor al que tiende x (h).

2. Puedes usar los botones interactivos para insertar símbolos matemáticos directamente.

3. Símbolos soportados:
     RAIZ: √(x)
     VALOR ABSOLUTO: |x|
     PI: π
     INFINITO: ∞ o -∞
     FUNCIONES: sen(x), cos(x), tan(x)
"""
        # Caja de texto (solo lectura) para mostrar la información de INICIO
        caja = ctk.CTkTextbox(self.tab_portada, width=800, height=350, font=("Arial", 12))
        caja.pack(pady=20)
        caja.insert("1.0", texto) # Inserta el texto desde la primera línea
        caja.configure(state="disabled") # Bloquea la caja para que el usuario no pueda editar el texto

    # --- MÉTODO: CONFIGURAR EL LIENZO DEL GRÁFICO ---
    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    # --- MÉTODOS AUXILIARES: BOTONES DE TECLADO ---
    def insertar_en_funcion(self, texto):
        # Inserta un símbolo matemático en la caja de texto de f(x) donde esté el cursor.
        posicion_cursor = self.f_x.index(ctk.INSERT)
        self.f_x.insert(posicion_cursor, texto)

    def insertar_en_h(self, texto):
        # Inserta un símbolo en la caja de texto del valor h (tendencia de x).
        posicion_cursor = self.tiende_h.index(ctk.INSERT)
        self.tiende_h.insert(posicion_cursor, texto)

    # --- MÉTODO: INTERFAZ DE LA CALCULADORA ---
    def crear_calculadora_limites(self):
        contenedor = ctk.CTkFrame(self.tab_Calculadora_limites)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel izquierdo (Controles)
        panel = ctk.CTkFrame(contenedor, width=380)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        # Panel derecho (Grafico)
        grafico_frame = ctk.CTkFrame(contenedor)
        grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- SECCIÓN DE ENTRADA: f(x) ---
        ctk.CTkLabel(panel, text="Control de Cálculo", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(panel, text="Función f(x):").pack()

        self.f_x = ctk.CTkEntry(panel, placeholder_text="Ej: (x**2-1)/(x-1)", width=250)
        self.f_x.pack(pady=5)

        # Teclado en pantalla para f(x)
        teclado_frame = ctk.CTkFrame(panel, fg_color="transparent")
        teclado_frame.pack(pady=5)

        # Lista de botones (Texto que se ve en el botón, Texto que se escribe)
        botones_herramientas = [
            ("√", "√("),
            ("|x|", "|"),
            ("π", "π"),
            ("∞", "∞"),
            ("sen", "sen("),
            ("cos", "cos(")
        ]

        # Creación de los botones en formato de cuadrícula (Grid) 3x2
        fila = 0
        columna = 0
        for texto_visual, texto_a_insertar in botones_herramientas:
            btn = ctk.CTkButton(
                teclado_frame, 
                text=texto_visual, 
                width=50, 
                height=30,
                font=("Arial", 14, "bold"),
                command=lambda t=texto_a_insertar: self.insertar_en_funcion(t)
            )
            btn.grid(row=fila, column=columna, padx=3, pady=3)
            
            columna += 1
            if columna > 2: # Si llega a la 3ra columna, baja de línea
                columna = 0
                fila += 1

        # --- SECCIÓN DE ENTRADA: Tendencia (h) ---
        ctk.CTkLabel(panel, text="Valor h (tiende a):").pack(pady=(10,0))
        self.tiende_h = ctk.CTkEntry(panel, placeholder_text="Ej: 1, π o ∞", width=250)
        self.tiende_h.pack(pady=5)

        # Teclado en pantalla para h
        teclado_h_frame = ctk.CTkFrame(panel, fg_color="transparent")
        teclado_h_frame.pack(pady=2)

        botones_h = [("∞", "∞"), ("-∞", "-∞"), ("π", "π")]
        col_h = 0
        for texto_visual, texto_a_insertar in botones_h:
            btn_h = ctk.CTkButton(
                teclado_h_frame, 
                text=texto_visual, 
                width=40, 
                height=25,
                font=("Arial", 12, "bold"),
                command=lambda t=texto_a_insertar: self.insertar_en_h(t)
            )
            btn_h.grid(row=0, column=col_h, padx=3, pady=3)
            col_h += 1

        # Botón principal para ejecutar el cálculo
        ctk.CTkButton(panel, text="Calcular y Graficar", command=self.ejecutar_calculo).pack(pady=20)

        # Cuadro de texto donde se mostrarán los resultados y el procedimien
        self.resultado_txt = ctk.CTkTextbox(panel, width=340, height=300)
        self.resultado_txt.pack(pady=10, padx=10)

        # Inicializamos el gráfico en el panel derecho
        self.figura, self.eje, self.canvas = self.crear_canvas(grafico_frame)

# --- MÉTODO: IMPRIMIR RESULTADOS ---
    def limpiar_y_escribir(self, texto):
        # Borra la consola de resultados y escribe el texto nuevo.
        self.resultado_txt.configure(state="normal") # Habilita la escritura
        self.resultado_txt.delete("1.0", "end") # Borra todo
        self.resultado_txt.insert("end", texto) # Inserta lo nuevo
        self.resultado_txt.configure(state="disabled") # Vuelve a bloquear la edición al usuario

    # --- CONTROLADOR PRINCIPAL DEL CÁLCULO ---
    def ejecutar_calculo(self):
        """Función puente recibe los datos del usuario, los traduce para SymPy y llama a las funciones lógicas."""
        enunciado_f = self.f_x.get()
        valor_h_str = self.tiende_h.get()
        
        try:
            x = sp.Symbol('x') # Define 'x' como variable matemática para SymPy
            
            # --- TRADUCCIÓN DE SÍMBOLOS ---
            # SymPy necesita formato en inglés, así que reemplazamos el formato en español.
            enunciado_f = enunciado_f.replace("π", "pi")
            enunciado_f = enunciado_f.replace("∞", "oo")
            enunciado_f = enunciado_f.replace("√", "sqrt")
            enunciado_f = enunciado_f.replace("sen", "sin")
            enunciado_f = enunciado_f.replace("cos", "cos")
            # Usa Expresiones Regulares para transformar |x| en Abs(x)
            enunciado_f = re.sub(r'\|([^|]+)\|', r'Abs(\1)', enunciado_f)
            
            # Convierte el string de texto en una función matemática evaluable
            f = sp.sympify(enunciado_f)
            
            # Procesar el valor de tendencia (h)
            h_str = valor_h_str.lower().strip()
            if h_str in ["oo", "inf", "∞"]: h = sp.oo
            elif h_str in ["-oo", "-inf", "-∞"]: h = -sp.oo
            else: h = sp.sympify(h_str.replace("π", "pi"))

            # --- LLAMADA A LA LÓGICA MATEMÁTICA ---
            pasos, res_final = self.calcular_limites_logica(f, h, x)
            asintotas_info = self.analizar_asintotas(f, x)
            
            # Formatea y muestra todo en el cuadro de texto
            info_completa = pasos + "\n" + "-"*30 + "\n" + asintotas_info
            self.limpiar_y_escribir(info_completa)
            
            # Genera la grafica
            self.graficar(f, h, x)

        except Exception as e:
            # Si hay un error de sintaxis u otro, lo muestra en rojo o en la consola
            self.limpiar_y_escribir(f"Error: {e}")

    # --- MÉTODO: LÓGICA PASO A PASO DEL LÍMITE ---
    def calcular_limites_logica(self, f, h, x):
        """Calcula el límite paso a paso: Valor absoluto, evaluación directa, simplificación y tabla de valores."""
        pasos = [f"--- ANÁLISIS DE LÍMITE ---\nx tiende a: {h}\n"]
        
        # 1. Valor Absoluto
        if f.has(sp.Abs) and h.is_finite:
            pasos.append(f"Paso {len(pasos)}: Análisis lateral por Valor Absoluto...\n")
            # Evalúa el límite acercándose por la izquierda (-0.0001) y derecha (+0.0001)
            izq = f.subs(x, float(h) - 0.0001).evalf(4)
            der = f.subs(x, float(h) + 0.0001).evalf(4)
            # Si los resultados por izquierda y derecha son diferentes, no existe limite
            if abs(izq - der) > 0.1:
                return "".join(pasos) + f"Límites lateral por izquierda = {izq} \n Limite lateral por derecha = {der}\nResultado: NO EXISTE", None

        # 2. Evaluación directa
        try:
            res = f.subs(x, h) # Intenta sustituir la 'x' por el valor 'h'
            if res.is_finite and not res.has(sp.nan):# Si el resultado es un número válido (no indeterminado)
                pasos.append(f"Paso {len(pasos)}: Evaluación directa exitosa.\nResultado = {res}")
                return "".join(pasos), res
        except: pass

        # 3. Simplificación algebraica 
        f_can = sp.cancel(f) # SymPy simplifica la fracción
        if f_can != f: # Si logró simplificar algo
            pasos.append(f"Paso {len(pasos)}: Simplificación detectada.\nNueva f(x): {f_can}\n")
            res = f_can.subs(x, h)
            if res.is_finite: return "".join(pasos) + f"Resultado = {res}", res

# --- NUEVA ESTRATEGIA: CONVERGENCIA NUMÉRICA (TABLA DE VALORES) ---
        # Utilizamos la técnica de la Guía 6: acercarse a h (Estrategia de aproximación numérica para indeterminaciones)
        if not res.is_finite or res.has(sp.nan):
            pasos.append(f"Paso {len(pasos)}: Indeterminación detectada. Aplicando Método de Aproximación Numérica (Tabla de Valores)...\n")
            
            # Solo si h es un número finito
            if h.is_finite:
                # Encabezado de la tabla
                pasos.append(f"{'Dirección':<12} | {'x':<12} | {'f(x)':<12}\n")
                pasos.append("-" * 40 + "\n")

                # Valores cada vez más pequeños para acercarse a 'h'
                epsilon = [0.1, 0.01, 0.001, 0.0001]
                v_izq, v_der = 0, 0
                
                for e in epsilon:
                    # Calculamos valores muy cercanos a h
                    x_izq = float(h) - e # Nos acercamos por la izquierda
                    x_der = float(h) + e # Nos acercamos por la derecha
                    
                    try:
                        # Calculamos los valores de la función y los convertimos a float
                        f_izq = float(f.subs(x, x_izq).evalf())
                        f_der = float(f.subs(x, x_der).evalf())
                        
                        # Añadimos las filas a la tabla
                        pasos.append(f"{'Izquierda':<12} | {x_izq:<12.4f} | {f_izq:<12.6f}\n")
                        pasos.append(f"{'Derecha':<12} | {x_der:<12.4f} | {f_der:<12.6f}\n")
                        
                        v_izq, v_der = f_izq, f_der
                    except:
                        continue
                
                # Comprobamos si los valores por ambos lados convergen (son casi iguales)
                if abs(v_izq - v_der) < 0.001:
                    resultado_aprox = round(v_izq, 2)
                    pasos.append(f"\nConclusión: f(x) converge a {resultado_aprox} por ambos lados.\n")
                    return "".join(pasos), resultado_aprox
                else:
                    pasos.append("\nConclusión: Los valores no convergen. El límite podría no existir o ser infinito.\n")
                    return "".join(pasos), sp.oo
    # --- MÉTODO: BÚSQUEDA DE ASÍNTOTAS ---
    def analizar_asintotas(self, f, x):
        info = "--- ANÁLISIS DE ASÍNTOTAS ---\n"
        num, den = sp.fraction(f) # Separa la función en numerador y denominador
        
        # Asíntotas Verticales (Raíces del denominador), Se buscan igualando el denominador a 0
        try:
            raices = sp.solve(den, x) # Encuentra las raíces del denominador
            if raices:
                info += f"A. Verticales en x = {raices}\n"
            else:
                info += "No se detectaron A. Verticales.\n"
        except: info += "Error buscando A. Verticales.\n"

        # Asíntotas Horizontales (Límite al infinito). Se analizan comparando los grados de los polinomios
        try:
            # Aqui Obtiene y analizamos el grado de x en numerador y denominador
            deg_num = sp.degree(num, x) if hasattr(num, 'as_poly') else 0
            deg_den = sp.degree(den, x) if hasattr(den, 'as_poly') else 0
            
            if deg_num < deg_den:
                info += "A. Horizontal en y = 0\n" # Si grado del denominador es mayor
            elif deg_num == deg_den:
                #  Si son iguales, es la división de los coeficientes principales
                lc_num = sp.Poly(num, x).LC()
                lc_den = sp.Poly(den, x).LC()
                info += f"A. Horizontal en y = {lc_num/lc_den}\n"
            else:
                info += "No tiene A. Horizontal (crece al infinito).\n"
        except: info += "Análisis de A. Horizontal no aplicable.\n"
        
        return info

# --- DIBUJAR LA GRÁFICA (Graficamos)---
    def graficar(self, f, h_val, x_sym):
        """Genera el gráfico en el Canvas. Se utiliza un ciclo for manual (sin Numpy) por regla del proyecto."""
        self.eje.clear() # Limpia la gráfica anterior
        
        # Rango de gráfico (SIN NUMPY). Determina el centro del gráfico (el valor de h, si es finito, o 0)
        try: centro = float(h_val) if h_val.is_finite else 0
        except: centro = 0
        
        # Listas para almacenar coordenadas (x, y)
        puntos_x = []
        puntos_y = []
        inicio = centro - 10 # Se grafica 10 unidades a la izquierda
        paso = 0.1 # Incremento de 0.1 en 0.1 (Requerimiento: Ciclo Manual)

        # Generamos 200 puntos (10 unidades a la izquierda y 10 a la derecha)
        for i in range(200):
            vx = inicio + (i * paso) # Calculamos valor de X actual
            try:
                vy = float(f.subs(x_sym, vx).evalf()) # Calculamos el valor de Y
                if -50 < vy < 50: # Evitar que el gráfico se dispare (evita que la gráfica se distorsione en las asíntotas)
                    puntos_x.append(vx)
                    puntos_y.append(vy)
                else: # Si se va al infinito, cortamos la línea metiendo un None
                    puntos_x.append(vx); puntos_y.append(None)
            except: 
                puntos_x.append(vx); puntos_y.append(None)

        # Dibuja la curva principal
        self.eje.plot(puntos_x, puntos_y, label="f(x)", color="#1f77b4")
        
        # Graficar Asíntotas Verticales (líneas rojas punteadas)
        num, den = sp.fraction(f)
        try:
            for r in sp.solve(den, x_sym):
                if r.is_real: # Solo grafica si la raíz es un número real
                    self.eje.axvline(x=float(r), color='red', linestyle=':', label='A.V.')
        except: pass

        # Marca con un punto naranja el valor al que tiende el límite (h)
        if h_val.is_finite:
            self.eje.scatter([float(h_val)], [0], color='orange', zorder=5, label=f"Tendencia x={h_val}")

        # Configuración estética del gráfico (Ejes X e Y en color negro, leyenda y cuadrícula)
        self.eje.axhline(0, color='black', lw=1)
        self.eje.axvline(0, color='black', lw=1)
        self.eje.legend(fontsize='small')
        self.eje.grid(True, alpha=0.3) # Activa la cuadrícula (grid)
        self.canvas.draw() # Actualiza y muestra el gráfico en Tkinter

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
# Este bloque verifica si el archivo se está ejecutando directamente
if __name__ == "__main__":
    app = CalculadoraLimites() # Crea una instancia de la aplicación
    app.mainloop() # Inicia el bucle infinito para mantener la ventana abierta