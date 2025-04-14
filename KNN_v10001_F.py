import csv
import random
import math
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

def cargar_datos(nombre_archivo):
    """
    Carga los datos desde un archivo CSV, moviendo la cuarta columna al final.
    
    Parámetros:
    - nombre_archivo: Ruta del archivo CSV a cargar.
    
    Retorna:
    - Una lista de listas con los datos cargados y modificados.
    """
    datos = []
    with open(nombre_archivo, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        encabezados = next(lector_csv)  # Omitir encabezados si es necesario
        for fila in lector_csv:
            fila = list(map(float, fila)) #Convierte en punto flotantes
            cuarta_columna = fila.pop(3) #Elimina la cuarta columna
            fila.append(cuarta_columna) #La fila contendra el elemento final de la cuarta columna
            datos.append(fila) #Se añade a datos una lista adicional de datos
    return datos

def dividir_datos(datos, proporcion_entrenamiento):
    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    
    Parámetros:
    - datos: Lista de datos a dividir.
    - proporcion_entrenamiento: Proporción del conjunto de entrenamiento.
    
    Retorna:
    - Tupla con dos listas: conjunto de entrenamiento y conjunto de prueba.
    """
    random.shuffle(datos) # Selecciona aleatoriamente los datos 
    num_muestras = len(datos) # Calcula el numero total de datos y devuelve la longitud (total de muestras)
    num_entrenamiento = int(num_muestras * proporcion_entrenamiento) # Calcula el numero de muestras 
    return datos[:num_entrenamiento], datos[num_entrenamiento:] #Devuelve dos sublistas de la lista datos

def distancia_euclidiana(punto1, punto2):
    """
    Calcula la distancia euclidiana entre dos puntos.
    
    Parámetros:
    - punto1: Primer punto como lista o tupla de coordenadas.
    - punto2: Segundo punto como lista o tupla de coordenadas.
    
    Retorna:
    - Distancia euclidiana entre punto1 y punto2.
    """
    return math.sqrt(sum([(x - y) ** 2 for x, y in zip(punto1, punto2)])) 

def KNN(conjunto_entrenamiento, punto_prueba, K):
    """
    Predice la clase de un punto de prueba utilizando el algoritmo k-NN.
    
    Parámetros:
    - conjunto_entrenamiento: Lista de puntos de entrenamiento.
    - punto_prueba: Punto de prueba para clasificar.
    - K: Número de vecinos más cercanos a considerar.
    
    Retorna:
    - La clase predicha para el punto de prueba.
    """
    vecinos_cercanos = sorted(conjunto_entrenamiento, key=lambda x: distancia_euclidiana(x[:-1], punto_prueba[:-1]))[:K] # Funcion lambda que calcula la distancia euc. entre un punto del conjunto de entrenamiento y un punto de prueba (toma todo excepto la ultima clase play) y hace lo mismo con el punto de prueba) y ordena el conjunto segun la DE
    clases_vecinos = [vecino[-1] for vecino in vecinos_cercanos] # Extrae el ultimo elemento de la lista vecinos_cercanos y lo almacena en la lista clases_vecinos
    return max(set(clases_vecinos), key=clases_vecinos.count) # devuelve el elemento mas comun dentro de la lista clases_vecinos

def evaluar_modelo(conjunto_entrenamiento, conjunto_prueba, k):
    """
    Evalúa el rendimiento del modelo k-NN en el conjunto de prueba.
    
    Parámetros:
    - conjunto_entrenamiento: Lista de puntos de entrenamiento.
    - conjunto_prueba: Lista de puntos de prueba.
    - k: Número de vecinos más cercanos a considerar.
    
    Retorna:
    - Precisión del modelo como un valor flotante.
    
    
    Itera sobre cada punto en el conjunto de prueba (conjunto_prueba). Para cada punto, se utiliza la función KNN (K-Nearest Neighbors) para predecir su clase 
    utilizando el conjunto de entrenamiento (conjunto_entrenamiento) y el valor de k dado. Si la clase predicha coincide con la clase real del punto, se suma 1.
    Esto cuenta el número total de aciertos.

    Devuelve la longitud total del conjunto de prueba, es decir, el número total de puntos en el conjunto de prueba.

    Finalmente, se calcula la tasa de aciertos dividiendo el número total de aciertos (aciertos) por el número total 
    de puntos en el conjunto de prueba. Esto devuelve la proporción de puntos clasificados correctamente en el conjunto de prueba.
    
    """
    
    aciertos = sum(1 for punto_prueba in conjunto_prueba if punto_prueba[-1] == KNN(conjunto_entrenamiento, punto_prueba, k)) #Itera 
    return aciertos / len(conjunto_prueba)

def cargar_datos_desconocidos():
    """
    Carga los datos desconocidos desde un archivo CSV seleccionado por el usuario.
    
    Retorna:
    - DataFrame de pandas con los datos desconocidos cargados.
    """
    
    ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")]) #El usuario selecciona un archivo CSV.
    
    if ruta_archivo: #Verifica si se ha seleccionado un archivo
        # Si se ha seleccionado un archivo, lee el contenido del archivo CSV en un DataFrame de Pandas llamado 'datos_desconocidos'.
        datos_desconocidos = pd.read_csv(ruta_archivo)
        # Devuelve el DataFrame 'datos_desconocidos' que contiene los datos del archivo CSV seleccionado.
        return datos_desconocidos
    # Si no se ha seleccionado ningún archivo (ruta_archivo está vacío), devuelve None.
    return None


def mostrar_resultados_clasificacion(resultados):
    """
    Muestra los resultados de clasificación en una nueva ventana.
    
    Parámetros:
    - resultados: Lista de resultados de clasificación para mostrar.
    """

    # Se crea una nueva ventana secundaria utilizando la clase Toplevel de Tkinter.
    ventana_resultados = tk.Toplevel()
    ventana_resultados.title("Resultados de predicción del partido de golf")
    ventana_resultados.geometry("600x400")

    # Crear un Frame como contenedor
    contenedor = ttk.Frame(ventana_resultados)
    contenedor.pack(fill=tk.BOTH, expand=True)

    # Crear el Treeview dentro del contenedor (muestra los datos en forma de tabla)
    tabla_resultados = ttk.Treeview(contenedor, columns=("Clasificación de predicción",), show="headings")
    tabla_resultados.heading("#1", text="Clasificación")
    tabla_resultados.column("#1", anchor=tk.CENTER)

    # Insertar los resultados en el Treeview (muestra datos en forma de tabla)
    for i, resultado in enumerate(resultados):
        clasificacion = "Sí" if resultado == 1 else "No"  # Cambiar 1 a "Sí" y 0 a "No"
        tabla_resultados.insert("", tk.END, values=(clasificacion,))

    # Crear Scrollbar y asociarlo con el Treeview
    scrollbar = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=tabla_resultados.yview)
    tabla_resultados.configure(yscrollcommand=scrollbar.set)

    # Colocar el Treeview y el Scrollbar en el contenedor
    tabla_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Función para mostrar las 20 iteraciones en una ventana con los resultados promedio de rendimiento
def mostrar_iteraciones(iteraciones, promedios_rendimiento):
    """
   Muestra las iteraciones y los resultados promedio de rendimiento en una nueva ventana.
   
   Parámetros:
   - iteraciones: Lista de iteraciones para mostrar.
   - promedios_rendimiento: Diccionario con los promedios de rendimiento.
   """
   # Crea una ventana para mostrar las iteraciones y los resultados promedio del rendimiento
    ventana_iteraciones = tk.Toplevel()
    ventana_iteraciones.title("20 Iteraciones y Resultados Promedio de Rendimiento")
    ventana_iteraciones.geometry("900x700")  # Establecer tamaño personalizado
    ventana_iteraciones.configure(bg='#ADD8E6')  # Fondo azul claro para la ventana

    # Configurar estilo para los widgets dentro de esta ventana
    estilo = ttk.Style()
    estilo.configure('TFrame', background='#ADD8E6')
    estilo.configure('TLabel', font=('Helvetica', 16), background='#ADD8E6', foreground='black')
    estilo.configure('TScrollbar', background='#ADD8E6')

    # Crear un marco para los resultados promedio a la derecha
    frame_resultados = ttk.Frame(ventana_iteraciones, style='TFrame')
    frame_resultados.pack(side="right", padx=10, pady=10, fill="y", expand=False)

    etiqueta_resultados = ttk.Label(frame_resultados, text="Resultados promedio de rendimiento:", font=("Helvetica", 14, 'bold'), background='#ADD8E6', foreground='black')
    etiqueta_resultados.pack()

    for k, rendimiento_promedio in promedios_rendimiento.items():
        etiqueta = ttk.Label(frame_resultados, text=f'{k}: {rendimiento_promedio:.2f}', font=("Helvetica", 16), background='#ADD8E6', foreground='black')
        etiqueta.pack(anchor="e")

    # Crear un widget Text para las iteraciones con un Scrollbar para el desplazamiento
    text_iteraciones = tk.Text(ventana_iteraciones, font=("Helvetica", 15), wrap="word", height=10, bd=0, padx=10, pady=10, bg="#E1E1E1", fg="black")
    scrollbar_iteraciones = ttk.Scrollbar(ventana_iteraciones, orient="vertical", command=text_iteraciones.yview, style='TScrollbar')
    text_iteraciones.configure(yscrollcommand=scrollbar_iteraciones.set)

    # Insertar texto de iteraciones en el widget Text
    text_iteraciones.insert(tk.END, "\n".join(iteraciones))
    text_iteraciones.config(state=tk.DISABLED)  # Deshabilitar edición

    # Empaquetar el widget Text y el Scrollbar
    text_iteraciones.pack(side="left", fill="both", expand=True)
    scrollbar_iteraciones.pack(side="left", fill="y")


# Función para manejar la clasificación y mostrar los resultados en la GUI
def clasificar_datos(conjunto_entrenamiento, k_entry):
    """
    Maneja la clasificación de datos desconocidos y muestra los resultados.
    
    Parámetros:
    - conjunto_entrenamiento: Lista de puntos de entrenamiento.
    - k_combobox: Widget Combobox de donde se obtiene el valor de K seleccionado.
    """
    
    datos_desconocidos = cargar_datos_desconocidos() # Carga el conjunto de datos
    if datos_desconocidos is not None: # Verifica que se cargaron correctamente
        resultado = [] # Si es correcto, se inicializa un lista vacia.
        
        k = int(k_entry.get())  # Obtiene el valor de K ingresado manualmente
        for _, fila in datos_desconocidos.iterrows(): # Itera sobre cada fila 
            punto_prueba = fila.values[:-1]  # Obtiene las caracteristicas de la fila excluyendo la última columna
            clase_predicha = KNN(conjunto_entrenamiento, punto_prueba, k) # Utiliza el algoritmo KNN para predecir la clase del punto de prueba
            resultado.append(clase_predicha) # Agrega la clase predicha a los resultados
        mostrar_resultados_clasificacion(resultado) # Llama a una funcion para mostrar los resultados
     
             
     
def mostrar_archivo_csv(ruta_archivo):
    
    """
   Abre una nueva ventana para mostrar el contenido de un archivo CSV en formato de tabla.
   
   Parámetros:
   - ruta_archivo: Ruta del archivo CSV a mostrar.
   """
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Vista de Archivo CSV")
    ventana_tabla.geometry("800x600")

    # Configurar el estilo de los widgets
    estilo = ttk.Style()
    # Guardar la configuración original del estilo
    original_font = estilo.lookup("Treeview", "font")
    original_rowheight = estilo.lookup("Treeview", "rowheight")

    # Configurar el estilo de los widgets para esta ventana
    estilo.configure("Treeview",
                     background="#D3D3D3",
                     foreground="black",
                     rowheight=25,  # Aumenta el rowheight si es necesario para acomodar el tamaño de la fuente
                     fieldbackground="#D3D3D3",
                     font=('Arial', 14))  # Aumenta el tamaño de la fuente aquí

    estilo.map('Treeview', background=[('selected', '#347083')])

    # Estilo para el Treeview Heading (cabecera)
    estilo.configure("Treeview.Heading",
                     font=('Arial', 16, 'bold'),  # Ajusta la fuente para los encabezados
                     background="#8B0000",
                     foreground="white")
    estilo.map('Treeview.Heading', background=[('active', '#B22222')])

    # Leer los datos del archivo CSV
    try:
        datos = pd.read_csv(ruta_archivo)
    except Exception as e:
        print("Error al leer el archivo CSV:", e)
        return

    # Crear el Treeview con Scrollbar
    frame = ttk.Frame(ventana_tabla)
    frame.pack(fill=tk.BOTH, expand=True)

    tabla = ttk.Treeview(frame, columns=list(datos.columns), show="headings", style="Treeview")
    tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    for columna in datos.columns:
        tabla.heading(columna, text=columna)
        tabla.column(columna, anchor=tk.CENTER)

    # Insertar los datos en el Treeview
    for _, fila in datos.iterrows():
        tabla.insert("", tk.END, values=tuple(fila))

    def on_closing():
        """Restablece el estilo original cuando la ventana se cierra."""
        estilo.configure("Treeview", font=original_font, rowheight=original_rowheight)
        ventana_tabla.destroy()

    ventana_tabla.protocol("WM_DELETE_WINDOW", on_closing)


    
# Función principal
def main():
    """
    Función principal que inicia la aplicación GUI.
    """
    nombre_archivo = 'archivo_modificado.csv' # Lee el archivo
    datos = cargar_datos(nombre_archivo) # Carga los datos del archivo
    num_iteraciones = 20 # Numero de iteraciones
    proporcion_entrenamiento = .218   # 10 / 14 (tamaño del conjunto de entrenamiento / tamaño total)
    promedios_rendimiento = {'K = 3': 0, 'K = 5': 0, 'K = 7': 0} # Diccionario para almacenar los promedios de rendimiento segun el K
    iteraciones = [] # Almacena las iteraciones

    resultados_por_iteracion = [] # Almacena los resultados de las iteraciones

    for _ in range(num_iteraciones): # Itera el numero de veces necesarias
        rendimientos = {} # Diccionario para almacenar los rendimientos de K
        conjunto_entrenamiento, conjunto_prueba = dividir_datos(datos, proporcion_entrenamiento) # Divide los datos (Entrenamiento y prueba)
        for k in [3, 5, 7]: # Para cada valor de K evalua el modelo y almacena el rendimiento 
            rendimiento = evaluar_modelo(conjunto_entrenamiento, conjunto_prueba, k)
            rendimientos[f'K = {k}'] = rendimiento
            promedios_rendimiento[f'K = {k}'] += rendimiento / num_iteraciones # Calcula el promedio de rendimiento y lo actualiza en el diccionario
         
            for k in [3, 5, 7]:
                promedios_rendimiento[f'K = {k}']+= promedios_rendimiento[f'K = {k}']/num_iteraciones
            
         
        resultados_por_iteracion.append(rendimientos) # Agrega los rendimiento de la iteracion actual a la lista de resultados por cada iteracion
    # Encuentra el mejor K basado en el promedio de rendimiento
    mejor_k = max(promedios_rendimiento, key=promedios_rendimiento.get)
    mejor_promedio = promedios_rendimiento[mejor_k]

    iteraciones.append("\ni\tK = 3 \t\tK = 5 \t\tK = 7 ") # Agrega el encabezado 
    for i, resultados in enumerate(resultados_por_iteracion, start=1): # Itera sobre los resultados y los muestra correspondiendo al rendimiento para cada valor de K
        rendimientos_i = [resultados[f'K = {k}'] for k in [3, 5, 7]] # Extrae los rendimientos para cada valor de K en la iteracion actual 
        iteraciones.append(f"\n{i}\t{rendimientos_i[0]:.2f}\t\t{rendimientos_i[1]:.2f}\t\t{rendimientos_i[2]:.2f}") # Construye una cadena que muestra el indice de la iteracion y los rendimientos para cada valor de K

    ventana_principal = tk.Tk()
    ventana_principal.title("Clasificación K-NN")
    ventana_principal.geometry("700x500")  # Ajustado para una mejor visualización
    ventana_principal.configure(bg='#ADD8E6')  # Fondo azul claro

    # Configuración del estilo para los widgets
    estilo = ttk.Style()
    estilo.theme_use('clam')  # Usar un tema que permita personalización
    estilo.configure('TLabel', font=('Helvetica', 14), background='#ADD8E6')
    estilo.configure('TButton', font=('Helvetica', 14), padding=10)
    estilo.configure('TCombobox', font=('Helvetica', 14))
    ventana_principal.option_add('*TCombobox*Listbox.font', ('Helvetica', 14))  # Ajusta el tamaño de la fuente de los ítems del Combobox

    etiqueta_principal = ttk.Label(ventana_principal, text='Implementación del Algoritmo KNN', font=("Helvetica", 18), background='#ADD8E6')
    etiqueta_principal.pack(pady=20)

    etiqueta_mejor_k = ttk.Label(ventana_principal, text=f'El mejor promedio fue {mejor_k} = {mejor_promedio:.2f}', font=("Helvetica", 16), background='#ADD8E6')
    etiqueta_mejor_k.pack(pady=10)

    boton_cargar_datos = ttk.Button(ventana_principal, text="Cargar Datos a Clasificar", command=lambda: clasificar_datos(datos, k_entry), style='TButton')
    boton_cargar_datos.pack(pady=10)

    boton_mostrar_iteraciones = ttk.Button(ventana_principal, text="Mostrar las 20 iteraciones", command=lambda: mostrar_iteraciones(iteraciones, promedios_rendimiento), style='TButton')
    boton_mostrar_iteraciones.pack(pady=10)

        
    etiqueta_k = ttk.Label(ventana_principal, text="Ingresa el valor de K: \n (Solo 3, 5 o 7)", font=("Helvetica", 14), background='#ADD8E6')
    etiqueta_k.pack(pady=10)
    
    k_entry = ttk.Entry(ventana_principal, font=('Helvetica', 14))
    k_entry.pack(pady=10)


    boton_abrir_modificado = ttk.Button(ventana_principal, text="Abrir Archivo Modificado", command=lambda: mostrar_archivo_csv('archivo_modificado.csv'))
    boton_abrir_modificado.pack(pady=10)

    boton_abrir_desconocidos = ttk.Button(ventana_principal, text="Abrir Datos Desconocidos", command=lambda: mostrar_archivo_csv('Desconocidos.csv'))
    boton_abrir_desconocidos.pack(pady=10)

    ventana_principal.mainloop()

    # Si el script se ejecuta como programa principal (es decir, no se está importando como 
    #un módulo en otro script), entonces se llama a la función main() para iniciar la ejecución del programa.
if __name__ == "__main__":
    main()