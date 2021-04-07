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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Sorting import shellsort as she
from DISClib.Algorithms.Sorting import quicksort as qui
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

#=========================================
# Construcción de modelos
#=========================================

def newCatalog():
    catalog = {'videos': None,
                'categories': None,
                'ctry':None,
                'cat-id': None,
                'paises': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['categories'] = lt.newList('ARRAY_LIST', comparecatnames)
    catalog["cat-id"] = mp.newMap(33,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareMapcatId)                                  
    catalog['paises'] = mp.newMap(50,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareMapcountry)
    return catalog

#================================================
# Funciones para agregar información al catálogo
#================================================

def addVideo(catalog, video):
    """ Agrega un video al final del catálogo.

    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

        video: diccionario con la información
        del video. 
    """
    lt.addLast(catalog['videos'], video)

    addVidCat(catalog, video)
    addCountry(catalog,video)

def addVidCat(catalog, video):
    """ Agrega un video al final del catálogo.
    
    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

        video: diccionario con la información
        del video. 
    """
    try:
        categorias = catalog['cat-id']
        cat_vid = video['category_id']
        existcat = mp.contains(categorias, cat_vid)
        if existcat:
            entry = mp.get(categorias, cat_vid)
            key = me.getKey(entry)
            categoria = me.getValue(entry)
            mp.put(catalog['cat-id'], key, categoria)
        lt.addLast(categoria['videos'], video)
    except Exception:
        return None

def addCountry(catalog,video):
    """ Agrega un video al final del catálogo.
    
    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

        video: diccionario con la información
        del video. 
    """
    try:
        paises = catalog['paises']
        paistend= video['country']
        existpais = mp.contains(paises, paistend)
        if existpais:
            entry = mp.get(paises, paistend)
            pais = me.getValue(entry)
        else:
            pais = newpais(paistend)
            mp.put(paises, paistend, pais)
        lt.addLast(pais['videos'], video)

    except Exception:
        return None

def newpais(paistend):
    entry= {'videos': None}
    entry['videos']= lt.newList('ARRAY_LIST')
    return entry
    
def addCategory(catalog, category):
    """ Agrega un video al final de la lista de categorias
        en el catálogo.
    
    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

        categoria: diccionario con la información
        de la categoría. 
    """
    c1= newCategoryL(category['name'], category['id'])
    c = newCategory(category['name'], category['id'])
    lt.addLast(catalog['categories'], c1)
    mp.put(catalog['cat-id'], category['id'], c)

#=========================================
# Funciones para creación de datos
#=========================================

def newCategoryL(category_name, category_id):
    """ Se crea un nuevo diccionario para cada categoría
        en el cual se guarda el id y el nombre de la
        categoría.

    Parámetros:
        category_name: es el nombre de la categoría.

        category_id: es el id de la categoría.

    Return:
        Un diccionario con la informacion de la categoria.
    """
    category = {'category_name': '', 'category_id': ''}
    category['category_name'] = category_name.lower()
    category['category_id'] = category_id
    return category

def newCategory(category_name, category_id):
    """ Se crea un nuevo diccionario para cada categoría
        en el cual se guarda el id y el nombre de la
        categoría.
    
    Parámetros:
        category_name: es el nombre de la categoría.

        category_id: es el id de la categoría.

    Return:
        Un diccionario con la información de la categoria.
    """
    category = {'category_name': '',
                 'category_id': '',
                 'videos': None}
    
    category['category_name'] = category_name.lower()
    category['category_id'] = category_id
    category['videos'] = lt.newList('ARRAY_LIST')
    return category

#=========================================
# Funciones de consulta/filtrado
#=========================================

def paisyCat(catalog, pais, cat_num):
    """
    """
    t1 = time.process_time()
    keys = mp.keySet(catalog['paises'])
    print(keys)
    key_value = mp.get(catalog['paises'], pais)
    value = me.getValue(key_value)
    lta = filtrado_categoria(value['videos'], cat_num)
    return lta

def consultaCat(catalog, categoria, num):
    """
    """
    t1 = time.process_time()
    #id_video = ''
    #lista = catalog['categories']
    #size = lt.size(lista)
    #for i in range(size):
    #    video = lt.getElement(lista, i)
    #    if video['category_name'] == categoria:
    #        id_video = video['category_id']

    keys = mp.keySet(catalog['cat-id'])
    key_value = mp.get(catalog['cat-id'], categoria)
    value = me.getValue(key_value)
    if num == 1:
        lista = sortVideosReq4(value['videos'])
    elif num == 3:
        lista = sortDate(value['videos'])
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    print('Tiempo: ' + str(tiempo_ms))
    return lista

def filtrado_pais(catalog, pais):
    """ Filtra los datos y hace una lista nueva
    con los datos del pais ingresado.

    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.
        
        pais: el país ingresado por el usuario.
    
    Return:
        Una lista con la información del pais
        ingresado.
    """
    lista_pais = lt.newList("ARRAY_LIST")
    for video in lt.iterator(catalog["videos"]):
        if video["country"] == pais:
            lt.addLast(lista_pais, video)
    return lista_pais

def filtrado_categoria(lista, categoria):
    """ Filtra los datos y hace una lista nueva
    con los datos de la categoría ingresada.

    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.
        
        categoria: la categoría ingresada por el usuario.
    
    Return:
        Una lista con la información de la categoría
        ingresada.
    """
    lista_filt_cat= lt.newList("ARRAY_LIST")
    for video in lt.iterator(lista):
        if video["category_id"] == categoria:
            lt.addLast(lista_filt_cat,video)
    return lista_filt_cat

def filtrado_tags(lista, tag):
    """ Filtra los datos y hace una lista nueva
    con los datos del pais y del tag ingreado.

    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

        tag: el tag ingresado por el usuario.
        
        pais: el país ingresado por el usuario.
    
    Return:
        Una lista con la información del pais y
        del tag ingresado.
    """
    lista_tags_y_pais = lt.newList('ARRAY_LIST')
    for video in lt.iterator(lista):
        tags = video['tags']
        if (tag in tags):
            lt.addLast(lista_tags_y_pais, video)
    return lista_tags_y_pais

def idCat(catalog, categoria):
    """ Encuentra el id de la categoria que entra por
        parametro.

    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.
        
        categoria: nombre de la categoria en la
        cual el usuario desea hacer su busqueda.

    Return:
        El int que corresponde a la categoria ingresada
        por parámetro.
    """
    num_cat = 31
    for kategorien in lt.iterator(catalog["categories"]):
        if categoria == kategorien["category_name"]:
            num_cat = kategorien["category_id"]
    return num_cat

def trending(videos_ordenados):
    """ Recorre la lista ordenada y cuenta cuántas
        veces se repite un id. La condición: si se 
        encuentran dos videos con el mismo id, 
        el contador aumenta, sino, no.

    Parámetros:
        videos_ordenados: es la lista ordenada que 
        se va a recorer.
    
    Return:
        Una tupla en la que la primera posición
        es las veces que apareció en la lista
        (días en trending) y la segunda posisición
        es el video que estuvo más días en trending.
    """    
    posicion = 0
    veces = 1
    mayor = 1
    size = lt.size(videos_ordenados)
    i = 0
    while i < size:
        if i != size:
            id_video = lt.getElement(videos_ordenados, i)
            id_video_2 = lt.getElement(videos_ordenados, i + 1)
            
            if (id_video['title'] == id_video_2['title']) :
                if (id_video['trending_date'] != id_video_2['trending_date']):
                    veces += 1
            else: 
                if veces > mayor:
                    mayor = veces
                    posicion = i
                veces = 1
            i += 1
        else:
            if i == size:
                break
    
    video = lt.getElement(videos_ordenados, posicion)
    return (mayor, video)

def trending_2(videos_ordenados):
    """ Recorre la lista ordenada y cuenta cuántas
        veces se repite un id. La condición: si se 
        encuentran dos videos con el mismo id, 
        el contador aumenta, sino, no.

    Parámetros:
        videos_ordenados: es la lista ordenada que 
        se va a recorer.
    
    Return:
        Una tupla en la que la primera posición
        es las veces que apareció en la lista
        (días en trending) y la segunda posisición
        es el video que estuvo más días en trending.
    """    
    posicion = 0
    veces = 1
    mayor = 1
    size = lt.size(videos_ordenados)
    i = 0
    while i < size:
        if i != size:
            id_video = lt.getElement(videos_ordenados, i)
            id_video_2 = lt.getElement(videos_ordenados, i + 1)
            
            if (id_video['video_id'] == id_video_2['video_id']):
                    veces += 1
            else: 
                if veces > mayor:
                    mayor = veces
                    posicion = i
                veces = 1
            i += 1
        else:
            if i == size:
                break
    
    video = lt.getElement(videos_ordenados, posicion)
    return (mayor, video)
   
def consultaMapaReq2(catalog, pais):
    """ Entra en el mapa y ordena los videos según la
        función de ordenamiento especificada (en este
        caso es sortVideosReq2(), es decir, ordena
        dependiendo del id del video).
    
    Parámetros:
        catalog: es el catálogo donde está toda la
        información cargada.

        pais: es el nombre del pais que el usuario
        ingresa.
    
    Retorna:
        Una tupla, en el que la primera posición
        ([0]) es el tiempo que tarda la función
        en ordenar, y la segunda es la lista
        ordenada.
    """
    t1 = time.process_time()
    lista_ordenada = lt.newList('ARRAY_LIST')
    #keys = mp.keySet(catalog['paises'])
    key_value = mp.get(catalog['paises'], pais)
    value = me.getValue(key_value)
    lista_ordenada = sortVideosReq2(value['videos'])
    t2 = time.process_time()
    tiempo_ms = (t2-t1) * 1000
    #print('Tiempo: ' + str(tiempo_ms))
    return lista_ordenada

def consultaMapaReq3(catalog, categoria):
    """ Entra en el mapa y ordena los videos según la
        función de ordenamiento especificada (en este
        caso es sortVideosReq4(), es decir, ordena
        dependiendo del número de likes).
    
    Parámetros:
        catalog: es el catálogo donde está toda la
        información cargada.

        categoria: es el nombre de la categoría que
        ingresa el usuario.
    
    Retorna:
        Una tupla, en el que la primera posición
        ([0]) es el tiempo que tarda la función
        en ordenar, y la segunda es la lista
        ordenada.
    """
    t1 = time.process_time()
    lista_ordenada = lt.newList('ARRAY_LIST')
    id_video = ''
    lista = catalog['categories']
    size = lt.size(lista)
    for i in range(size):
        video = lt.getElement(lista, i)
        if video['category_name'] == categoria:
            id_video = video['category_id']
    #id_video = idCat(catalog, categoria)

    #keys = mp.keySet(catalog['cat-id'])
    key_value = mp.get(catalog['cat-id'], id_video)
    value = me.getValue(key_value)
    lista_ordenada = sortVideosReq4(value['videos'])
    t2 = time.process_time()
    tiempo_ms = (t2-t1) * 1000
    #print('Tiempo: ' + str(tiempo_ms))
    return lista_ordenada

def consultaMapaReq4(catalog, pais):
    """ Entra en el mapa y ordena los videos según la
        función de ordenamiento especificada (en este
        caso es sortVideosReq4(), es decir, ordena
        dependiendo del número de likes).
    
    Parámetros:
        catalog: es el catálogo donde está toda la
        información cargada.

        pais: es el nombre del pais que el usuario
        ingresa.
    
    Retorna:
        Una tupla, en el que la primera posición
        ([0]) es el tiempo que tarda la función
        en ordenar, y la segunda es la lista
        ordenada.
    """
    t1 = time.process_time()
    lista_ordenada = lt.newList('ARRAY_LIST')
    #keys = mp.keySet(catalog['paises'])
    key_value = mp.get(catalog['paises'], pais)
    value = me.getValue(key_value)
    lista_ordenada = sortVideosReq4(value['videos'])
    t2 = time.process_time()
    tiempo_ms = (t2-t1) * 1000
    #print('Tiempo: ' + str(tiempo_ms))
    return lista_ordenada

#==========================================================================
# Funciones utilizadas para comparar elementos dentro de una/un lista/mapa
#==========================================================================

def comparecatnames(category_name, category):
    """ Compara el nombre de la categoria que entra
        por parametro con uno de los que ya se encuentran
        en el catálogo.

    Parámetros:
        category_name: es el nombre de la categoría que
        se quiere comparar.

        category: es la sección del catálogo de donde se
        saca el nombre de la categoría.

    Retorna:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si el nombre
        ingresado por parámetro es igual al que está
        en el catálogo).
    """
    return (category_name == category['category_name'])

def compareMapcountry(Id, entry):
    """
    """
    identry= me.getKey(entry)
    if Id == identry:
        return 0
    elif Id > identry:
        return 1
    else:
        return -1
    #return  (pais1 == pais2)

def compareviews(video1, video2):
    """ Compara el número de 'views' que tiene
        un video.

    Parámetros:
        video1: es una lista de videos de donde se 
        ven los views para comparar.

        video2: es una lista de videos de donde se 
        ven los views para comparar.
    
    Return:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si las 'views'
        del video1 son mayores que las del video2).
    """
    result = (video1["views"] > video2["views"])
    return result

def comparetitle(video1, video2):
    """ Compara el 'title' que tiene un video.

    Parámetros:
        video1: es una lista de videos de donde se 
        ve el id para comparar.

        video2: es una lista de videos de donde se 
        ve el id para comparar.
    
    Return:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si el 'id'
        del video1 es 'mayor' al del video2).
    """
    result = (video1['title'] > video2['title'])
    return result

def compareMapcatId(Id, entry):
    """
    """
    identry= me.getKey(entry)
    if int(Id) == int(identry):
        return 0
    elif int(Id) > int(identry):
        return 1
    else:
        return -1

def comparedates(video1, video2):
    """ Compara las fechas en trending que tiene
        un video.

    Parámetros:
        video1: es una lista de videos de donde se 
        ve la fecha de trending para comparar.

        video2: es una lista de videos de donde se 
        ve la fecha de trending para comparar.
    
    Return:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si la fecha
        del video1 es menor que la del video2).
    """
    result = video1['trending_date'] < video2['trending_date']
    return result

def comparelikes(video1, video2):
    """ Compara el número de 'likes' que tiene
        un video.

    Parámetros:
        video1: es una lista de videos de donde se 
        ven los likes para comparar.

        video2: es una lista de videos de donde se 
        ven los likes para comparar.
    
    Return:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si los 'likes'
        del video1 son mayores que los del video2).
    """
    result = int(video1['likes']) > int(video2['likes'])
    return result

def compareids(video1, video2):
    """ Compara el id que tiene un video.

    Parámetros:
        video1: es una lista de videos de donde se 
        ve el id para comparar.

        video2: es una lista de videos de donde se 
        ve el id para comparar.
    
    Return:
        Un booleano que indica si sí se cumple la
        condición (en este caso, True si el id
        del video1 es mayor que el del video2).
    """
    result = video1['video_id'] > video2['video_id']
    return result

def lista(catalog):
    """ Retorna la lista de los videos
    
    Parámetros:
        catalog: el catálogo principal creado
        en la función 'newCatalog()'.

    Return: 
        La lista de los videos que se encuentra dentro del catalogo
    """
    lista = catalog["videos"]
    return lista

#=========================================
# Funciones de ordenamiento
#=========================================

def sortVideos(lista):
    """ Función sort para ordenar los videos con
        las condiciones de la cmpfunction. En este
        caso, la función de comparación es:
                    compareviews().

    Parámetros:
        lista: es la lista que se va a ordenar.
    
    Return:
        Una tupla en la que la primera posición
        es el tiempo que tarde la función en ordenar
        y la segunda posición es la lista ordenada.
    """
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = mer.sort(sub_list, compareviews)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

def sortVideosReq2(lista):
    """ Función sort para ordenar los videos con
        las condiciones de la cmpfunction. En este
        caso, la función de comparación es:
                    compareids().

    Parámetros:
        lista: es la lista que se va a ordenar.
    
    Return:
        Una tupla en la que la primera posición
        es el tiempo que tarde la función en ordenar
        y la segunda posición es la lista ordenada.
    """
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = mer.sort(sub_list, compareids)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

def sortVideosReq3(lista):
    """ Función sort para ordenar los videos con
        las condiciones de la cmpfunction. En este
        caso, la función de comparación es:
                    compareids().

    Parámetros:
        lista: es la lista que se va a ordenar.
    
    Return:
        Una tupla en la que la primera posición
        es el tiempo que tarde la función en ordenar
        y la segunda posición es la lista ordenada.
    """
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = mer.sort(sub_list, comparetitle)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

def sortDate(lista):
    """ Función sort para ordenar los videos con
        las condiciones de la cmpfunction. En este
        caso, la función de comparación es:
                    comparedates().

    Parámetros:
        lista: es la lista que se va a ordenar.
    
    Return:
        Una tupla en la que la primera posición
        es el tiempo que tarde la función en ordenar
        y la segunda posición es la lista ordenada.
    """
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = mer.sort(sub_list, comparedates)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

def sortVideosReq4(lista):
    """ Función sort para ordenar los videos con
        las condiciones de la cmpfunction. En este
        caso, la función de comparación es:
                    comparelikes().

    Parámetros:
        lista: es la lista que se va a ordenar.
    
    Return:
        Una tupla en la que la primera posición
        es el tiempo que tarde la función en ordenar
        y la segunda posición es la lista ordenada.
    """
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = qui.sort(sub_list, comparelikes)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

def limpieza(lista):
    """ Esta funcion recibe como parametro cualquier
        tipo de dato que es requerido temporalmente 
        y lo retorna none para evitar que se llene la
        memoria RAM.

    Parámetros:
        lista: es la lista que se va a limpiar.

    Retorna:
        La lista que queda vacía (None).
    """
    lista = None
    return lista
