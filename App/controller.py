"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc
from datetime import datetime


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initCatalog():
    catalog = model.newCatalog()
    return catalog

#=========================================
# Funciones para la carga de datos
#=========================================

def loadData(catalog):
    # Respuestas por defecto
    delta_time = -1.0
    delta_memory = -1.0

    # Inicializa el proceso para medir memoria
    tracemalloc.start()

    # Toma de tiempo y memoria al inicio del proceso
    star_time = getTime()
    start_memory = getMemory()

    loadCategory(catalog)
    loadVideos(catalog)
    
    # Toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # Finaliza el proceso para medir memoria
    tracemalloc.stop()

    # Calculando la diferencia de tiempo y memoria
    delta_time = stop_time - star_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadVideos(catalog):
    """Crea un diccionario con la informacion del video para que sea posteriormente agregado
    al catalogo en su lista correspondiente"""
    videosfile = cf.data_dir + 'videos-small.csv'
    input_file = csv.DictReader(open(videosfile, encoding='utf-8'))
    for video in input_file:
        filtrado = {}
        filtrado["video_id"] = video["video_id"]
        filtrado["trending_date"] = video["trending_date"]
        filtrado["title"] = video["title"]
        filtrado["channel_title"] = video["channel_title"]
        filtrado["category_id"] = int(video["category_id"])
        filtrado["publish_time"] = video["publish_time"]
        filtrado["tags"] = video["tags"]
        filtrado["country"] = video["country"]
        filtrado["views"] = int(video["views"])
        filtrado["likes"] = int(video["likes"])
        filtrado["dislikes"] = int(video["dislikes"])
        filtrado['trending_date'] = video['trending_date']
        filtrado['publish_time'] = video['publish_time']
        model.addVideo(catalog, filtrado)

def loadCategory(catalog):
    """Crea un diccionario con la informacion de la categoria
    para que sea posteriormente agregado
    al catalogo en su lista correspondiente"""
    categoriesfile = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(categoriesfile, encoding='utf-8'))
    for category in input_file:
        category_list = category['id\tname'].split('\t')
        category['name'] = category_list[1]
        category['id'] = int(category_list[0])
        model.addCategory(catalog, category)

#=========================================
# Funciones de ordenamiento
#=========================================

def sortVideos(lista):
    """Llama a la funcion sortVideos del modelo"""
    return model.sortVideos(lista)

def sortVideosReq2(lista):
    """Llama a la funcion sortVideosReq2 del modelo"""
    return model.sortVideosReq2(lista)

def sortVideosReq3(lista):
    """Llama a la funcion sortVideosReq3 del modelo"""
    return model.sortVideosReq3(lista)

def sortDate(lista):
    return model.sortDate(lista)
    
def sortVideosReq4(lista):
    """Llama a la funcion 'sortVideosReq4()' del modelo"""
    return model.sortVideosReq4(lista)

def limpieza(lista):
    """Llama a la funcion 'limpieza()' del modelo"""
    return model.limpieza(lista)

#=========================================
# Funciones de consulta sobre el catálogo
#=========================================
def paisyCat(catalog, pais, cat_num):
    return model.paisyCat(catalog, pais, cat_num)

def filtrado_pais(catalog, pais):
    """Llama a la funcion 'filtrado_pais()' del modelo"""
    return model.filtrado_pais(catalog, pais)

def lista(catalog):
    """Llama a la funcion 'lista()' del modelo"""
    return model.lista(catalog)
    
def filtrado_categoria(lista, categoria):
    """Llama a la funcion 'filtrado_categoria()' del modelo"""
    return model.filtrado_categoria(lista, categoria)

def filtrado_tags(catalog, tag):
    """Llama a la funcion 'filtrado_categoria()' del modelo"""
    return model.filtrado_tags(catalog, tag)

def idCat(catalog, categoria):
    return model.idCat(catalog, categoria)

def trending(lista):
    return model.trending(lista)

def trending_2(lista):
    return model.trending_2(lista)

#=========================================
# Función LAB 6
#=========================================
def consultaCat(catalog, categoria,num):
    return model.prueba(catalog, categoria)

def prueba(catalog, categoria):
    return model.prueba(catalog, categoria)

#==============================================
# Funciones para medir tiempo y uso de memoria
#==============================================

def getTime():
    """
    Devuelve el instante de tiempo de procesamiento
    en milisegundos.
    """
    return float(time.perf_counter() * 1000)

def getMemory():
    """
    Toma una muestra de la memoria alocada en el
    instante de tiempo.
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    Calcula la diferencia en memoria alocada en el
    programa entre dos instantes de tiempo y devuelve
    el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, 'filename')
    delta_memory = 0.0

    # Suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    
    # De Byte -> kByte:
    delta_memory = delta_memory / 1024.0
    return delta_memory