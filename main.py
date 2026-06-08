def transformar_valor_absoluto(funcion_texto):
    while "|" in funcion_texto:
        funcion_texto = funcion_texto.replace("|", "abs(", 1)
        if "|" in funcion_texto:
            funcion_texto = funcion_texto.replace("|", ")", 1)
        else:
            print("Error: Olvidaste cerrar una barra de valor absoluto '|'.")
            return None
            
    return funcion_texto

entrada_usuario = input("Ingresa la función (ejemplo: |x**2 - 9| / (x - 3)): ")

funcion_usuario = transformar_valor_absoluto(entrada_usuario)

def calcular_y(x):
    if funcion_usuario is None:
        return None
    try:
        return eval(funcion_usuario)
    except ZeroDivisionError:
        return None
    except Exception as e:
        print(f"Error al evaluar la función. Detalle: {e}")
        return None

def evaluar_limite(tendencia):
    if funcion_usuario is None:
        return
        
    h = 1e-9  
    
    x_izq = tendencia - h
    x_der = tendencia + h
    
    y_izq = calcular_y(x_izq)
    y_der = calcular_y(x_der)
    
    if y_izq is None or y_der is None:
        print("\n=> No se pudo calcular el límite.")
        return

    print(f"\nFunción interpretada internamente: {funcion_usuario}")
    print(f"Evaluando por la izquierda (x = {x_izq:.9f}) -> y = {y_izq:.5f}")
    print(f"Evaluando por la derecha   (x = {x_der:.9f}) -> y = {y_der:.5f}")
    
    if round(y_izq, 4) == round(y_der, 4):
        print(f"\n=> El límite general existe y es aproximadamente: {round(y_izq, 4)}")
    else:
        print("\n=> El límite general NO existe (los límites laterales son distintos).")

try:
    ten = float(input("Ingresa la tendencia: "))
    evaluar_limite(ten)
except ValueError:
    print("Por favor, ingresa un número válido para la tendencia.")