# Generador de Fotomosaicos en Python

## Archivos Incluidos

- `10000 images.zip`: Carpeta con subcarpetas de imágenes diversas para aplicar en el fotomosaico.  
  **⚠️ IMPORTANTE: DESCOMPRIMIR ESTE ARCHIVO PARA QUE EL PROGRAMA FUNCIONE CORRECTAMENTE.**  
- `fotomosaico.py`: Archivo de Python ejecutable.  
- `ReadMe.txt`: Archivo con la documentación del proyecto.  

## Salida del Programa

Al ejecutar el programa, se generarán los siguientes archivos:  

- `fotomosaico_resultado.jpg`: Imagen del fotomosaico generado.  
- `fotomosaico.html`: Archivo HTML para visualizar el fotomosaico.  
- `fotomosaico.txt`: Archivo con las medidas utilizadas para construir el fotomosaico.  
- `mosaic_parts/`: Carpeta con las imágenes generadas y ajustadas al tamaño adecuado para el fotomosaico.  

## Descripción del Proyecto

Este proyecto es una aplicación en Python que genera un **fotomosaico**.  
Un fotomosaico es una imagen compuesta por muchas imágenes más pequeñas (**mosaicos**) que, al combinarse, forman la imagen original.  

### Tecnologías Utilizadas
- **Pillow (PIL)**: Para la manipulación de imágenes.  
- **Tkinter**: Para la interfaz gráfica.  
- **NumPy**: Para cálculos matemáticos.  

### Método de Selección de Imágenes  
Se usa la **distancia euclidiana** para calcular la similitud entre las regiones de la imagen base y las imágenes de la biblioteca.  
Para esto, se usa la norma euclidiana de NumPy, que mide la diferencia entre los valores de color.  
La imagen con el promedio de color más cercano (menor distancia euclidiana) se selecciona como la más similar.  

---

## Requisitos

### Instalación de Dependencias  

Es necesario contar con **Python 3.x** y las siguientes bibliotecas:  

```sh
pip install pillow numpy
