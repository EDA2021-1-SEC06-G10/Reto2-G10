﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time 

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar y cargar información en el catálogo")
    print("2- Encontrar buenos videos")
    print("3- Encontrar tendencia por pais")
    print("4- Encontrar tendencia por categoria")
    print("5- Buscar los videos con mas likes")
    #print("(LAB) 6- Buscar los videos con mas likes por categoría")
    print("0- Salir")


def print_resultsReq1(ord_vids, sample):
    size = lt.size(ord_vids)
    if size > sample:
        print("Los primeros ", sample, " videos en views son: ")
        i = 1
        while i <= sample:
            video= lt.getElement(ord_vids,i)
            print("Titulo: " + video['title'] + " || " + " Fecha tendencia: " +  video["trending_date"] + " || " + " Canal: " + video["channel_title"] + " || " + " Momento de publicacion: " + video["publish_time"] + " || " + " Views: "+ str(video["views"]) + " || " + " Likes: " + str(video["likes"]) + " || " + " Dislikes: " + str(video["dislikes"]) + '.')
            i += 1

def print_resultsReq2(tupla):
    dias = tupla[0]
    video_tendencia = tupla[1]
    print("Titulo: " + video_tendencia['title'] + " || " + " Nombre del canal: " +  video_tendencia['channel_title'] + " || "  + ' País: ' + video_tendencia['country'] + " || " + ' Días: ' + str(dias) + '.')

def print_resultsReq3(tupla):
    dias = tupla[0]
    video = tupla[1]
    print("Titulo: " + video['title'] + " || " + " Nombre del canal: " +  video['channel_title'] + " || " + " Categoria: " + str(video['category_id']) + " || " + " Dias: " + str(dias) + '.')

def print_resultsReq4(ord_vids, sample):
    size = lt.size(ord_vids)
    if size > sample:
        print("Los " + str(sample) + " videos con más likes son: ")
        i = 1
        while i <= sample:
            video= lt.getElement(ord_vids,i)
            print("Titulo: " + video['title'] + " || " + " Nombre del canal: " + video["channel_title"] + " || " + " Momento de publicacion: " + video["publish_time"] + " || " + " Views: "+ str(video["views"]) + " || " + " Likes: " + str(video["likes"]) + " || " + " Dislikes: " + str(video["dislikes"]) + " || " + ' Tags: ' + video['tags'] + '.')
            i += 1
    else:
        print("La cantidad que desea ver excede la cantidad de videos que desea ver")

def initCatolog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Cargando información de los archivos .... ")
        #t1 = time.process_time_ns()
        catalog = initCatolog()
        answer = controller.loadData(catalog)
        #t2 = time.process_time_ns()
        #print("El tiempo transcurrido fue: "+ str(t2-t1))
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorías cargadas: ' + str(lt.size(catalog['categories'])))
        print('Tiempo [ms]: ', f'{answer[0]:.3f}', " || ", 
              'Memoria [kB]: ', f'{answer[1]:.3f}')

    elif int(inputs[0]) == 2: # Print Requerimiento 1
        pais = input("Ingrese el pais para el cual desea realizar la búsqueda: ")
        pais= pais.lower()
        categoria = input("Ingrese la categoria que desea conocer: ")
        categoria = categoria.lower()
        categoria = " " + categoria
        tamano = int(input("Ingrese la cantidad de videos que desea ver: "))
        num_categoria = controller.idCat(catalog, categoria)
        filtrado_categoria = controller.paisyCat(catalog, pais, num_categoria)
        result = controller.sortVideos(filtrado_categoria)
        print_resultsReq1(result[1], tamano)
        controller.limpieza(filtrado_categoria)
        controller.limpieza(result)

    elif int(inputs[0]) == 3: # Print Requerimiento 2
        pais = input('Ingrese el pais para el cual desea realizar la búsqueda: ')
        pais = pais.lower()
        lista_videos = controller.consultaMapaReq2(catalog, pais)
        video_tendencia = controller.trending_2(lista_videos[1])
        print_resultsReq2(video_tendencia)
        controller.limpieza(lista_videos)
        controller.limpieza(video_tendencia)

    elif int(inputs[0]) == 4: # Print Requerimiento 3
        categoria = input("Ingrese la categoria para la cual desea ver el video con mas dias como tendencia: ")
        categoria = categoria.lower()
        categoria = " " + categoria
        cat_num = controller.idCat(catalog, categoria)
        vids_cat = controller.consultaCat(catalog, categoria)
        orden_id = controller.sortVideosReq3(vids_cat[1])
        video_mayor = controller.trending(orden_id[1])
        print_resultsReq3(video_mayor)
        controller.limpieza(vids_cat)
        controller.limpieza(orden_id)

    elif int(inputs[0]) == 5: # Print Requerimiento 4
        pais = input("Ingrese el pais para el cual desea realizar la búsqueda: ")
        pais = pais.lower()
        tag = input("Ingrese el tag que desea que buscar (si es una palabra, importan las mayúsculas): " )
        sample = int(input("Ingrese la cantidad de video que desea ver: "))
        lista_likes = controller.filtro_tags(catalog, pais, tag)
        lista_videos = controller.sortVideosReq4(lista_likes)
        print_resultsReq4(lista_videos[1], sample)
        controller.limpieza(lista_videos)
        controller.limpieza(lista_likes)

    else:
        sys.exit(0)
sys.exit(0)
