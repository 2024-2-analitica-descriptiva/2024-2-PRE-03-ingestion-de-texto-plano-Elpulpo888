"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd

def pregunta_01():
    
    # Lectura del archivo
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    # Inicializar listas para almacenar los datos
    datos = []
    current_row = None  # Almacena la fila en construcción
    cluster_counter = 1  # Contador manual para clusters
    
    # Procesar las líneas del archivo, omitiendo las primeras cuatro líneas de encabezado
    for line in lines[4:]:
        if line.strip():  # Ignorar líneas vacías
            # Detectar si es una nueva fila (inicia con un número en la primera columna)
            if line[:4].strip().isdigit():
                if current_row:  # Si hay una fila en construcción, guardarla
                    datos.append(current_row)
                cluster = cluster_counter  # Asignar el contador actual al cluster
                cluster_counter += 1  # Incrementar el contador
                cantidad = int(line[5:18].strip())
                porcentaje = float(line[19:33].strip().replace(",", ".").replace("%", ""))
                palabras_clave = line[34:].strip()
                current_row = [cluster, cantidad, porcentaje, palabras_clave]
            else:
                # Es una continuación de la columna de palabras clave
                if current_row:
                    current_row[-1] += " " + line.strip()

    # Añadir la última fila procesada
    if current_row:
        datos.append(current_row)

    # Convertir a DataFrame
    df = pd.DataFrame(datos, columns=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"])

    # Limpiar la columna principales_palabras_clave
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace("\s+", " ", regex=True)  # Remover espacios extra
        .str.replace(", ", ",")              # Normalizar comas
        .str.replace(",", ", ")              # Espacio después de comas
        .str.strip()                         # Eliminar espacios iniciales y finales
        .str.rstrip(".")                     # Eliminar punto final
    )
    return df

   
