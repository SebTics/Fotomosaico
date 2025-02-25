import os  # Módulo para manejar operaciones del sistema de archivos
from tkinter import Tk, filedialog, Button, Label, Entry, messagebox  # Módulos para crear la interfaz gráfica
from PIL import Image  # Biblioteca para el manejo de imágenes
import numpy as np  # Biblioteca para operaciones matemáticas y de arrays

# Función para calcular la similitud entre dos regiones basándose en la distancia euclidiana
def calculate_similarity(region_avg, img_avg):
    return np.linalg.norm(region_avg - img_avg)

# Preprocesa la biblioteca de imágenes para generar una lista de imágenes y sus promedios de color
def preprocess_library(library_folder, tile_size):
    image_library = []  # Lista para almacenar las imágenes
    image_averages = []  # Lista para almacenar el promedio de colores de cada imagen

    # Iteramos sobre los archivos en la carpeta especificada
    for filename in os.listdir(library_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Filtra por formatos de imagen válidos
            img = Image.open(os.path.join(library_folder, filename))  # Abre la imagen
            img_resized = img.resize((tile_size, tile_size))  # Redimensiona la imagen al tamaño de mosaico
            img_avg = np.mean(np.array(img_resized), axis=(0, 1))  # Calcula el promedio de color de la imagen
            image_library.append(img_resized)  # Agrega la imagen redimensionada a la biblioteca
            image_averages.append(img_avg)  # Agrega el promedio de color a la lista de promedios

    # Verifica si la biblioteca contiene imágenes válidas
    if not image_library:
        raise Exception("La biblioteca de imágenes está vacía o no contiene formatos válidos.")
    
    return image_library, np.array(image_averages)

# Crea un fotomosaico a partir de una imagen base y una biblioteca de imágenes
def create_photomosaic(input_image_path, output_image_path, tile_size, library_folder):
    input_image = Image.open(input_image_path)  # Abre la imagen base
    input_width, input_height = input_image.size  # Obtiene el tamaño de la imagen base

    # Calculamos las dimensiones de la cuadrícula para el mosaico
    grid_width = input_width // tile_size
    grid_height = input_height // tile_size

    # Redimensionamos la imagen base para que se ajuste exactamente a la cuadrícula
    resized_image = input_image.resize((grid_width * tile_size, grid_height * tile_size))

    # Preprocesa la biblioteca de imágenes
    image_library, image_averages = preprocess_library(library_folder, tile_size)

    # Crea una nueva imagen en blanco para el fotomosaico
    mosaic_image = Image.new('RGB', resized_image.size)

    # Itera sobre cada región (celda) de la cuadrícula
    for y in range(grid_height):
        for x in range(grid_width):
            # Se define las coordenadas de la región actual
            left = x * tile_size
            top = y * tile_size
            right = left + tile_size
            bottom = top + tile_size
            region = resized_image.crop((left, top, right, bottom))  # Extrae la región de la imagen base

            # Calculamos el promedio de color de la región
            region_avg = np.mean(np.array(region), axis=(0, 1))

            # Encuentra la imagen más similar en la biblioteca
            similarities = np.linalg.norm(image_averages - region_avg, axis=1)  # Calcula similitudes
            best_match_index = np.argmin(similarities)  # Obtiene el índice de la mejor coincidencia
            best_match = image_library[best_match_index]  # Obtiene la imagen correspondiente

            # Pega la imagen seleccionada en la posición correspondiente
            mosaic_image.paste(best_match, (left, top))

    # Aquí guardamos la imagen final
    mosaic_image.save(output_image_path)
    return output_image_path

def generate_html_output(mosaic_image, output_html_path, library_folder, grid_width, grid_height, tile_size):
    """
    Genera un archivo HTML con una tabla que contiene las imágenes del fotomosaico.

    Args:
        mosaic_image: La imagen completa del mosaico.
        output_html_path: Ruta de salida para el archivo HTML.
        library_folder: Carpeta donde se guardan las partes del mosaico.
        grid_width: Número de mosaicos en X.
        grid_height: Número de mosaicos en Y.
        tile_size: Tamaño de cada mosaico.
    """
    # Asegúrate de que library_folder sea una ruta relativa
    relative_library_folder = os.path.relpath(library_folder)

    with open(output_html_path, "w") as file:
        file.write('<table border="0" cellspacing="0" cellpadding="0">\n')

        for y in range(grid_height):
            file.write("<tr>\n")
            for x in range(grid_width):
                # Calcular las coordenadas del recorte
                left = x * tile_size
                top = y * tile_size
                right = left + tile_size
                bottom = top + tile_size
                region = mosaic_image.crop((left, top, right, bottom))

                # Nombre del archivo recortado
                region_name = f"Im{y * grid_width + x}.jpg"
                region_path = os.path.join(library_folder, region_name)

                # Guardar la imagen recortada en la carpeta
                region.save(region_path)

                # Escribir el HTML con la ruta relativa a mosaic_parts
                file.write(f'<td><nobr><img src="{relative_library_folder}/{region_name}" width="10" height="10"></nobr></td>\n')
            file.write("</tr>\n")

        file.write('</table>\n')


def generate_txt_output(mosaic_image, output_txt_path, grid_width, grid_height, tile_size, output_folder="mosaic_parts"):
    # Crear la carpeta si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_txt_path, "w") as file:
        # Escribe las dimensiones y el tamaño de mosaicos en las primeras líneas
        file.write(f"{grid_width}\n")  # Cantidad de mosaicos en X
        file.write(f"{grid_height}\n")  # Cantidad de mosaicos en Y
        file.write(f"{tile_size}\n")  # Tamaño de cada subregión en X
        file.write(f"{tile_size}\n")  # Tamaño de cada subregión en Y
        file.write(f"{tile_size}\n")  # Tamaño de cada mosaico en X
        file.write(f"{tile_size}\n")  # Tamaño de cada mosaico en Y

        # Itera sobre la cuadrícula del mosaico
        for y in range(grid_height):
            for x in range(grid_width):
                left = x * tile_size
                top = y * tile_size
                right = left + tile_size
                bottom = top + tile_size

                # Recorta la región correspondiente del mosaico
                region = mosaic_image.crop((left, top, right, bottom))

                # Nombre del archivo generado para la región dentro de la carpeta
                region_name = f"Im{y * grid_width + x}.jpg"
                region_path = os.path.join(output_folder, region_name)

                # Guarda la región como una imagen separada en la carpeta especificada
                region.save(region_path)

                # Escribe el nombre del archivo (incluyendo la carpeta) en el archivo de texto
                file.write(f"{output_folder}/{region_name}\n")

            # Agrega el comando `<br>` después de cada fila de mosaicos (al completar la fila)
            if y < grid_height - 1:  # Evita añadir `<br>` al final del archivo
                file.write("<br>\n")
                
# Función para seleccionar la imagen base mediante un diálogo de selección
def select_image():
    global input_image_path
    input_image_path = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])  # Filtra por formatos de imagen
    if input_image_path:
        lbl_image_path.config(text=f"Imagen seleccionada: {input_image_path}")

# Función para seleccionar la carpeta de biblioteca mediante un diálogo de selección
def select_library():
    global library_folder
    library_folder = filedialog.askdirectory()  # Abre un diálogo para seleccionar una carpeta
    if library_folder:
        lbl_library_path.config(text=f"Carpeta seleccionada: {library_folder}")

# Función para generar el fotomosaico y manejar posibles errores
def generate_mosaic():
    try:
        tile_size = int(entry_tile_size.get())  # Obtiene el tamaño de los mosaicos desde la entrada
        if tile_size <= 0:
            raise ValueError("El tamaño del mosaico debe ser mayor a 0.")  # Valida el tamaño del mosaico
        if not input_image_path or not library_folder:
            messagebox.showerror("Error", "Selecciona la imagen y la carpeta de biblioteca.")  # Verifica selecciones
            return

        output_image_path = "fotomosaico_resultado.jpg"  # Nombre del archivo de salida
        result = create_photomosaic(input_image_path, output_image_path, tile_size, library_folder)

        # Obtener dimensiones del mosaico para la salida
        input_image = Image.open(input_image_path)
        input_width, input_height = input_image.size
        grid_width = input_width // tile_size
        grid_height = input_height // tile_size

        # Cargar la imagen generada del fotomosaico para trabajar con ella
        mosaic_image = Image.open(result)

        # Generar HTML
        html_output_path = "fotomosaico.html"
        generate_html_output(mosaic_image, html_output_path, library_folder, grid_width, grid_height, tile_size)

        # Generar archivo de texto
        txt_output_path = "fotomosaico.txt"
        generate_txt_output(mosaic_image, txt_output_path, grid_width, grid_height, tile_size)


        # Mostrar mensaje de éxito con las rutas de salida
        messagebox.showinfo("Éxito", f"Fotomosaico generado: {result}\nSalida HTML: {html_output_path}\nSalida TXT: {txt_output_path}")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))  # Muestra un mensaje de error en caso de fallos

# Configuración de la interfaz gráfica
root = Tk()  # Inicializa la ventana principal
root.title("FotoMosaicos")  # Título de la ventana
root.geometry("800x500")  # Tamaño de la ventana

# Widgets para seleccionar la imagen base
lbl_image_path = Label(root, text="Selecciona la imagen principal:")
lbl_image_path.pack(pady=5)
btn_select_image = Button(root, text="Seleccionar Imagen", command=select_image)
btn_select_image.pack(pady=5)

# Widgets para seleccionar la carpeta de biblioteca
lbl_library_path = Label(root, text="Selecciona la carpeta de imágenes de biblioteca:")
lbl_library_path.pack(pady=5)
btn_select_library = Button(root, text="Seleccionar Carpeta", command=select_library)
btn_select_library.pack(pady=5)

# Widgets para ingresar el tamaño de los mosaicos
lbl_tile_size = Label(root, text="Tamaño de cada mosaico (en píxeles):")
lbl_tile_size.pack(pady=5)
entry_tile_size = Entry(root)
entry_tile_size.pack(pady=5)

# Botón para generar el fotomosaico
btn_generate = Button(root, text="Generar Fotomosaico", command=generate_mosaic)
btn_generate.pack(pady=20)

# Variables globales para almacenar las selecciones
input_image_path = None
library_folder = None

# Inicia el bucle principal de la aplicación
root.mainloop()
