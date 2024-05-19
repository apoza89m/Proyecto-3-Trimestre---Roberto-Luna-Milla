from pymongo import MongoClient
import json
import os

# conn
client = MongoClient('localhost', 27017)

# dropear la base de datos
dblist = client.list_database_names()
if "sevilla_historica" in dblist:
  client.drop_database('sevilla_historica')
  print("La base de datos ha sido dropeada.")

db = client['sevilla_historica']
lugares_collection = db['lugares']
eventos_collection = db['eventos']
personajes_collection = db['personajes']
 
# cambiar ruta de trabajo
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# añade la coleccion lugares si esta vacia
if lugares_collection.count_documents({}) == 0:  
    print("Las coleccion 'lugares' esta vacia.")
    
    # verifica si el archivo  existe, debe estar en la misma carpeta
    ruta = os.path.join(ROOT_PATH, "lugares.json")
    if os.path.exists(ruta):
        with open(ruta) as file:
            file_data = json.load(file)
            print("JSON lugares cargado.")       
        if isinstance(file_data, list):
            lugares_collection.insert_many(file_data)  
        else:
            lugares_collection.insert_one(file_data)
    else:
        print("No existe el archivo", ruta)
else: 
    print("La coleccion 'lugares' ya existe.")

# añade la coleccion eventos si esta vacia
if eventos_collection.count_documents({}) == 0:  
    print("Las coleccion 'eventos' esta vacia.")
    
    # verifica si el archivo  existe, debe estar en la misma carpeta
    ruta = os.path.join(ROOT_PATH, "eventos.json")
    if os.path.exists(ruta):
        with open(ruta) as file:
            file_data = json.load(file)
            print("JSON eventos cargado.")       
        if isinstance(file_data, list):
            eventos_collection.insert_many(file_data)  
        else:
            eventos_collection.insert_one(file_data)
    else:
        print("No existe el archivo", ruta)
else: 
    print("La coleccion 'eventos' ya existe.")

# añade la coleccion personajes si esta vacia
if personajes_collection.count_documents({}) == 0:  
    print("Las coleccion 'personajes' esta vacia.")
    
    # verifica si el archivo  existe, debe estar en la misma carpeta
    ruta = os.path.join(ROOT_PATH, "personajes.json")
    if os.path.exists(ruta):
        with open(ruta) as file:
            file_data = json.load(file)
            print("JSON personajes cargado.")       
        if isinstance(file_data, list):
            personajes_collection.insert_many(file_data)  
        else:
            personajes_collection.insert_one(file_data)
    else:
        print("No existe el archivo", ruta)
else: 
    print("La coleccion 'personajes' ya existe.")


# opciones del menu
def opcion_1():
    while True: 
        print("Opcion 1: Dar de alta documento(s)")
        print("¿En que coleccion quieres dar de alta el documento?")
        print("1. Lugares")
        print("2. Eventos")
        print("3. Personajes")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            alta_lugar()
        elif opcion == "2":
            alta_evento()
        elif opcion == "3":
            alta_personaje()
        else:
            print("Opcion no valida.")
        continuar = input("¿Quiere agregar otro lugar? (s/n): ")
        if continuar.lower() != 's':
            break

def alta_lugar():
    nombre = input("Ingrese el nombre: ")
    descripcion = input("Ingrese la descripcion: ")
    ubicacion = input("Ingrese la ubicacion: ")
    fecha_construccion = input("Ingrese el año de construccion: ")
    horario = input("Ingrese el horario de apertura/cierre: ")
    telefono = input("Ingrese el telefono: ")
    total_visitas = input("Ingrese la cantidad de turistas que han visitado el lugar: ")

    lugar = {
        "nombre": nombre,
        "descripcion": descripcion,
        "ubicacion": ubicacion,
        "fecha_construccion": fecha_construccion,
        "horario": horario,
        "telefono": telefono,
        "total_visitas": total_visitas
    }

    lugares_collection.insert_one(lugar)
    print("Documento insertado.")

def alta_evento():
    nombre = input("Ingrese el nombre: ")
    descripcion = input("Ingrese la descripcion: ")
    epoca = input("Ingrese la epoca: ")
    siglo = input("Ingrese el siglo: ")
    lugar = input("Ingrese el lugar: ")

    evento = {
        "nombre": nombre,
        "descripcion": descripcion,
        "fecha": [{
            "epoca": epoca,
            "siglo": siglo
        }],
        "lugar": {
            "nombre": lugar
        }
    }

    eventos_collection.insert_one(evento)
    print("Documento insertado.")

def alta_personaje():
    nombre = input("Ingrese el nombre: ")
    biografia = input("Ingrese la biografía: ")
    epoca = input("Ingrese la epoca: ")
    anyo_nacimiento = input("Ingrese el año de nacimiento: ")
    anyo_muerte = input("Ingrese el año de muerte: ")
    lugar_nacimiento = input("Ingrese el lugar de nacimiento: ")
    eventos_destacados = []
    while True:
        evento_nombre = input("Ingrese el nombre de un evento destacado del personaje (deje vacío para terminar): ")
        if not evento_nombre:
            break
        eventos_destacados.append({"nombre": evento_nombre})

    personaje = {
        "nombre": nombre,
        "biografia": biografia,
        "epoca": epoca,
        "anyo_nacimiento": anyo_nacimiento,
        "anyo_muerte": anyo_muerte,
        "lugar_nacimiento": lugar_nacimiento,
        "eventos_destacados": eventos_destacados
    }

    personajes_collection.insert_one(personaje)
    print("Documento insertado.")

def opcion_2():
    while True:
        print("Opcion 2: Actualizar documento(s)")
        print("¿En que coleccion quieres actualizar el documento?")
        print("1. Lugares")
        print("2. Eventos")
        print("3. Personajes")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            actualizar_lugar()
        elif opcion == "2":
            actualizar_evento()
        elif opcion == "3":
            actualizar_personaje()
        else:
            print("Opcion no valida.")
        continuar = input("¿Quiere agregar otro documento? (s/n): ")
        if continuar.lower() != 's':
            break
    
def actualizar_lugar():
    filtro_nombre = input("Ingresa el nombre del lugar que quieres actualizar: ")

    lugar_actual = lugares_collection.find_one({"nombre": filtro_nombre})

    if lugar_actual:
        print("Ingrese los nuevos valores (deja en blanco si no quieres cambiar):")

        nuevo_nombre = input("Nuevo nombre: ")
        nueva_descripcion = input("Nueva descripcion: ")
        nueva_ubicacion = input("Nueva ubicacion: ")
        nuevo_fecha_construccion = input("Nuevo año de construccion: ")
        nuevo_horario = input("Nuevo horario de apertura/cierre: ")
        nuevo_telefono = input("Nuevo telefono: ")
        nueva_total_visitas = input("Nueva cantidad de visitas: ")

        campos_actualizados = {}

        if nuevo_nombre:
            campos_actualizados["nombre"] = nuevo_nombre
        if nueva_descripcion:
            campos_actualizados["descripcion"] = nueva_descripcion
        if nueva_ubicacion:
            campos_actualizados["ubicacion"] = nueva_ubicacion
        if nuevo_fecha_construccion:
            campos_actualizados["fecha_construccion"] = nuevo_fecha_construccion
        if nuevo_horario:
            campos_actualizados["horario"] = nuevo_horario
        if nuevo_telefono:
            campos_actualizados["telefono"] = nuevo_telefono
        if nueva_total_visitas:
            campos_actualizados["total_visitas"] = nueva_total_visitas

        lugares_collection.update_one({"nombre": filtro_nombre}, {"$set": campos_actualizados})
        print("Documento actualizado.")
    else:
        print("No existe lugar con ese nombre.")

def actualizar_evento():
    filtro_nombre = input("Ingresa el nombre del evento que quieres actualizar: ")

    evento_actual = eventos_collection.find_one({"nombre": filtro_nombre})

    if evento_actual:
        print("Ingresa los nuevos valores (deja en blanco si no quieres cambiar):")

        nuevo_nombre = input("Nuevo nombre: ")
        nueva_descripcion = input("Nueva descripcion: ")
        nueva_epoca = input("Nueva epoca: ")
        nuevo_siglo = input("Nuevo siglo: ")
        nuevo_lugar_nombre = input("Nuevo nombre del lugar: ")
        nuevo_participantes = input("Nuevos participantes (separe con comas si hay varios): ")

        campos_actualizados = {}

        if nuevo_nombre:
            campos_actualizados["nombre"] = nuevo_nombre
        if nueva_descripcion:
            campos_actualizados["descripcion"] = nueva_descripcion
        if nueva_epoca:
            campos_actualizados["fecha.0.epoca"] = nueva_epoca
        if nuevo_siglo:
            campos_actualizados["fecha.0.siglo"] = nuevo_siglo
        if nuevo_lugar_nombre:
            campos_actualizados["lugar.nombre"] = nuevo_lugar_nombre
        if nuevo_participantes:
            campos_actualizados["participantes"] = [participante.strip() for participante in nuevo_participantes.split(",")]

        eventos_collection.update_one({"nombre": filtro_nombre}, {"$set": campos_actualizados})
        print("Documento actualizado.")
    else:
        print("No existe evento con ese nombre.")

def actualizar_personaje():
    filtro_nombre = input("Ingresa el nombre del personaje que quieres actualizar: ")

    personaje_actual = personajes_collection.find_one({"nombre": filtro_nombre})

    if personaje_actual:
        print("Ingresa los nuevos valores (deja en blanco si no quieres cambiar):")

        nuevo_nombre = input("Nuevo nombre: ")
        nueva_biografia = input("Nueva biografia: ")
        nueva_epoca = input("Nueva epoca: ")
        nuevo_anyo_nacimiento = input("Nuevo año de nacimiento: ")
        nuevo_anyo_muerte = input("Nuevo año de muerte: ")
        nuevo_lugar_nacimiento = input("Nuevo lugar de nacimiento: ")
        nuevos_eventos_destacados = input("Nuevos eventos destacados (separe con comas si hay varios): ")

        campos_actualizados = {}

        if nuevo_nombre:
            campos_actualizados["nombre"] = nuevo_nombre
        if nueva_biografia:
            campos_actualizados["biografia"] = nueva_biografia
        if nueva_epoca:
            campos_actualizados["epoca"] = nueva_epoca
        if nuevo_anyo_nacimiento:
            campos_actualizados["anyo_nacimiento"] = nuevo_anyo_nacimiento
        if nuevo_anyo_muerte:
            campos_actualizados["anyo_muerte"] = nuevo_anyo_muerte
        if nuevo_lugar_nacimiento:
            campos_actualizados["lugar_nacimiento"] = nuevo_lugar_nacimiento
        if nuevos_eventos_destacados:
            eventos = [evento.strip() for evento in nuevos_eventos_destacados.split(",")]
            campos_actualizados["eventos_destacados"] = [{"nombre": evento} for evento in eventos]

        personajes_collection.update_one({"nombre": filtro_nombre}, {"$set": campos_actualizados})
        print("Documento actualizado.")
    else:
        print("No existe personaje con ese nombre.")

def opcion_3():
    print("Opcion 3: Eliminar documento en concreto")
    print("¿En que coleccion quieres eliminar el documento?")
    print("1. Lugares")
    print("2. Eventos")
    print("3. Personajes")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        eliminar_lugar()
    elif opcion == "2":
        eliminar_evento()
    elif opcion == "3":
        eliminar_personaje()
    else:
        print("Opcion no valida.")

def eliminar_lugar():
    nombre = input("Ingresa el nombre del lugar que quieres eliminar: ")

    lugar = lugares_collection.find_one({"nombre": nombre})

    if lugar:
        confirmacion = input(f"¿Esta seguro de que quieres eliminar el lugar '{nombre}'? (s/n): ").lower()
        if confirmacion == 's':
            lugares_collection.delete_one({"nombre": nombre})
            print("Documento eliminado.")
        else:
            print("Eliminacion cancelada.")
    else:
        print("No existe lugar con ese nombre.")

def eliminar_evento():
    nombre = input("Ingresa el nombre del evento que quieres eliminar: ")

    evento = eventos_collection.find_one({"nombre": nombre})

    if evento:
        confirmacion = input(f"¿Está seguro de que quieres eliminar el evento '{nombre}'? (s/n): ").lower()
        if confirmacion == 's':
            eventos_collection.delete_one({"nombre": nombre})
            print("Documento eliminado.")
        else:
            print("Eliminación cancelada.")
    else:
        print("No existe evento con ese nombre.")

def eliminar_personaje():
    nombre = input("Ingresa el nombre del personaje que quieres eliminar: ")

    personaje = personajes_collection.find_one({"nombre": nombre})

    if personaje:
        confirmacion = input(f"¿Está seguro de que quieres eliminar el personaje '{nombre}'? (s/n): ").lower()
        if confirmacion == 's':
            personajes_collection.delete_one({"nombre": nombre})
            print("Documento eliminado.")
        else:
            print("Eliminación cancelada.")
    else:
        print("No existe personaje con ese nombre.")

def opcion_4():
    print("Opcion 4: Mostrar todos los documentos de una coleccion")
    print("¿Que coleccion quieres mostrar?")
    print("1. Lugares")
    print("2. Eventos")
    print("3. Personajes")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        documentos = lugares_collection.find()
        print(f"Documentos en lugares:")
        for documento in documentos:
            for campo, valor in documento.items():
                print(f"{campo}: {valor}")
            print()
    elif opcion == "2":
        documentos = eventos_collection.find()
        print(f"Documentos en eventos:")
        for documento in documentos:
            for campo, valor in documento.items():
                print(f"{campo}: {valor}")
            print()
    elif opcion == "3":
        documentos = personajes_collection.find()
        print(f"Documentos en personajes:")
        for documento in documentos:
            for campo, valor in documento.items():
                print(f"{campo}: {valor}")
            print()                
    else:
        print("Opcion no valida.")

def opcion_5():
    print("Opcion 5: Busquedas")
    print("1. Buscar por ubicación en el Centro Histórico:")
    print("2. Eventos de la Edad Media:")
    print("3. Personajes nacidos en Sevilla:")
    print("4. Encontrar lugares con mas de 500 años de antigüedad:")
    print("5. Buscar eventos relacionados con la historia de la ciudad durante el siglo XIX")
    print("6. Buscar lugares con horario 'Siempre abierto'")
    opcion = input("Seleccione una opcion: ")

    if opcion == '1':
        query = { "ubicacion": { "$regex": "Centro", "$options": "i" } }
        resultados = lugares_collection.find(query)
        print("Lugares en centro historico:")
        for resultado in resultados:
            print(f"Nombre: {resultado['nombre']}")

    elif opcion == '2':
        query = {"fecha.epoca": "Edad Media"}
        resultados = eventos_collection.find(query)
        print("Eventos de la Edad Media:")
        for resultado in resultados:
            print(f"Nombre: {resultado['nombre']}")

    elif opcion == '3':
       query = { "lugar_nacimiento": { "$regex": "Sevilla", "$options": "i" } }
       resultados = personajes_collection.find(query)
       print("Personajes nacidos en Sevilla:")
       for resultado in resultados:
           print(f"Nombre: {resultado['nombre']}")

    elif opcion == '4':
        query = { "fecha_construccion": { "$lt": 1524 } }
        resultados = lugares_collection.find(query)
        print("Lugares con mas de 500 años de antigüedad:")
        for resultado in resultados:
            print(f"Nombre: {resultado['nombre']}")

    elif opcion == '5':
        query = {"fecha": { "$elemMatch": { "siglo": "XIX" } }}
        resultados = eventos_collection.find(query)
        print("Eventos relacionados con la historia de la ciudad durante el siglo XIX:")
        for resultado in resultados:
            print(f"Nombre: {resultado['nombre']}")

    elif opcion == '6':
        query = { "horario": { "$regex": "Siempre", "$options": "i" } }
        resultados = lugares_collection.find(query)
        print("Lugares con horario 'Siempre abierto':")
        for resultado in resultados:
            print(f"Nombre: {resultado['nombre']}")
    else:
        print("Opcion no valida.")
        return

def opcion_6():
    print("Opcion 6: Eliminar todos los elementos de una coleccion")
    print("¿Qué coleccion quieres vaciar?")
    print("1. Lugares")
    print("2. Eventos")
    print("3. Personajes")
    opcion = input("Elige una opcion: ")

    if opcion == "1":
        confirmar_vaciar_coleccion(lugares_collection)
    elif opcion == "2":
        confirmar_vaciar_coleccion(eventos_collection)
    elif opcion == "3":
        confirmar_vaciar_coleccion(personajes_collection)
    else:
        print("Opcion no valida.")

def confirmar_vaciar_coleccion(collection):
    confirmacion = input("¿Quiere eliminar todos los elementos de esta coleccion? (s/n): ").lower()
    if confirmacion == 's':

        collection.delete_many({})
        print("Se eliminaron todos los documentos de la coleccion: ",{collection.name})
    else:
        print("Eliminacion cancelada.")

def opcion_7():
    print("Opcion 7: Eliminar la coleccion")
    print("¿Que coleccion quieres eliminar?")
    print("1. Lugares")
    print("2. Eventos")
    print("3. Personajes")
    opcion = input("Elige una opcion: ")

    if opcion == "1":
        confirmar_eliminar_coleccion(lugares_collection)
    elif opcion == "2":
        confirmar_eliminar_coleccion(eventos_collection)
    elif opcion == "3":
        confirmar_eliminar_coleccion(personajes_collection)
    else:
        print("Opcion no valida.")

def confirmar_eliminar_coleccion(collection):
    confirmacion = input("¿Esta seguro de que quieres eliminar por completo esta coleccion? (s/n): ").lower()
    if confirmacion == 's':
        db.drop_collection(collection.name)
        print("La coleccion ",{collection.name}," fue eliminada correctamente.")
    else:
        print("Eliminacion cancelada.")

def opcion_9():
    print("1. Calcular el número total de lugares historicos en la base de datos:")
    print("2. Encontrar la época con más eventos históricos registrados:")
    print("3. Agrupar los eventos por siglo y contar cuántos hay en cada siglo:")
    print("4. Calcular el promedio de años de vida de los personajes históricos:")
    print("5. Encontrar los lugares más visitados por turistas y mostrar los cinco primeros:")
    print("6. Ordenar personajes por fecha de muerte con eventos:")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        pipeline = [{"$count": "total_lugares"}]
        resultado = list(lugares_collection.aggregate(pipeline))
        if resultado:
            print("Numero total de lugares historicos:", resultado[0]["total_lugares"])
        else:
            print("No se encontraron lugares historicos en la base de datos.")

    elif opcion == "2":
        pipeline = [{"$group": {"_id": "$fecha.epoca", "total_eventos":
        {"$sum": 1}}},
        {"$sort": {"total_eventos": -1}},
        {"$limit": 1}]
        resultado = list(eventos_collection.aggregate(pipeline))
        if resultado:
            print("Época con mas eventos históricos registrados:")
            print("Época:", resultado[0]["_id"])
            print("Total de eventos:", resultado[0]["total_eventos"])
        else:
            print("No se encontraron eventos históricos en la base de datos.")

    elif opcion == "3":
        pipeline = [
            {"$unwind": "$fecha"},
            {"$group": {"_id": "$fecha.siglo", "total_eventos": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        resultados = eventos_collection.aggregate(pipeline)
        print("Eventos agrupados por siglo:")
        for resultado in resultados:
            print("Siglo:", resultado["_id"])
            print("Total de eventos:", resultado["total_eventos"])

    elif opcion == "4":
        pipeline = [{"$match": {"anyo_nacimiento": {"$exists": True}, "anyo_muerte": {"$exists": True}}},
        {"$project": {"_id": 0, "vida": {"$subtract": ["$anyo_muerte", "$anyo_nacimiento"]}}},
        {"$group": {"_id": None, "promedio_vida": {"$avg": "$vida"}}}]
        resultados = personajes_collection.aggregate(pipeline)
        for resultado in resultados:
            promedio_vida = resultado["promedio_vida"]
            print("El promedio de años de vida es:", promedio_vida)

    elif opcion == "5":
        pipeline = [{"$match": {"total_visitas": {"$exists": True}}},
        {"$sort": {"total_visitas": -1}},
        {"$limit": 5}]
        resultados = lugares_collection.aggregate(pipeline)
        print("Los cinco lugares más visitados por turistas son:")
        for index, lugar in enumerate(resultados, start=1):
            print(f"{index}. {lugar['nombre']} - Visitantes: {lugar['total_visitas']}")

    elif opcion == "6":
        pipeline = [
        {"$lookup": {
            "from": "eventos",
            "localField": "eventos_destacados.nombre",
            "foreignField": "nombre",
            "as": "eventos_asociados"
        }},
        {"$match": {"eventos_asociados": {"$ne": []}}},
        {"$sort": {"anyo_muerte": 1}}
    ]
        resultados = personajes_collection.aggregate(pipeline)
        print("Personajes ordenados por fecha de muerte con eventos:")
        for index, personaje in enumerate(resultados, start=1):
            print(f"{index}. {personaje['nombre']} - Fecha de muerte: {personaje['anyo_muerte']}")
            if personaje['eventos_asociados']:
                print("   Eventos asociados:")
                for evento in personaje['eventos_asociados']:
                    print(f"   - {evento['nombre']}")

    else:
        print("Opcion no valida.")
    
def menu():
    while True:
        print("MENU")
        print("1. Dar de alta un/varios documentos")
        print("2. Actualizar un/varios documentos")
        print("3. Eliminar un documento en concreto")
        print("4. Mostrar todos los documentos de una coleccion")
        print("5. Busquedas")
        print("6. Eliminar todos los elementos de una coleccion")
        print("7. Eliminar la coleccion")
        print("8. Salir")
        print("9. Pipeline")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            opcion_1()
        elif opcion == "2":
            opcion_2()
        elif opcion == "3":
            opcion_3()
        elif opcion == "4":
            opcion_4()
        elif opcion == "5":
            opcion_5()
        elif opcion == "6":
            opcion_6()
        elif opcion == "7":
            opcion_7()
        elif opcion == "8":
            print("Saliendo...")
            break
        elif opcion == "9":
            opcion_9()
        else:
            print("Opcion no valida.")

# ejecuta el menu principal
menu()
