# Fotomosaico - Generador de Imágenes en Python  

## 📂 Archivos Incluidos  

- **Carpeta `10000 images`**: Contiene subcarpetas con imágenes diversas para aplicar en el fotomosaico.  
- **`fotomosaico.py`**: Archivo ejecutable de Python.  
- **`ReadMe.txt`**: Este archivo con la documentación.  

## 📌 Resultados Generados  

El programa genera los siguientes archivos como salida:  

- **`fotomosaico_resultado.jpg`** → Imagen del fotomosaico generado.  
- **`fotomosaico.html`** → Archivo HTML con la visualización del fotomosaico.  
- **`fotomosaico.txt`** → Documento de texto con las medidas utilizadas en las imágenes del fotomosaico.  
- **`mosaic_parts/`** → Carpeta con las imágenes ajustadas al tamaño adecuado para el fotomosaico.  

## 🖼️ Descripción  

Este proyecto es una aplicación en **Python** que permite generar un **fotomosaico**, es decir, una imagen formada por una colección de imágenes más pequeñas (mosaicos) que, al combinarse, crean la imagen original.  

Para ello, se utiliza:  

- **PIL (Pillow)** para manipulación de imágenes.  
- **Tkinter** para la interfaz gráfica.  
- **Distancia Euclidiana** para calcular la similitud entre las regiones de la imagen base y las imágenes de la biblioteca.  

La métrica de **Norma Euclidiana de NumPy** permite seleccionar la imagen más similar mediante la raíz cuadrada de la suma de los cuadrados de las diferencias entre los valores de color.  

## 📋 Requisitos  

Se requiere **Python 3.x** y las siguientes bibliotecas:  

```bash
pip install pillow numpy

