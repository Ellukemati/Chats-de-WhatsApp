import csv
import random

def partir_mensaje(linea: str) -> tuple:
# Particiona la línea del mensaje hasta conseguir los datos que son útiles
    if "<Multimedia omitido>" in linea:
        return None, None

    partes_linea = linea.rstrip().split(" - ")
    if len(partes_linea) != 2:
        return None, None

    datos_mensaje = partes_linea[1].split(":")
    if len(datos_mensaje) != 2:
        return None, None

    nombre, mensaje = datos_mensaje
    return nombre, mensaje

def contar_palabras(dirección: str) -> dict:
    contactos = {}

    with open(dirección, "r", encoding="utf-8") as chat:
        for linea in chat:
            nombre, mensaje = partir_mensaje(linea)

            if nombre and mensaje:
                if nombre not in contactos:
                    contactos[nombre] = {}

                palabras = mensaje.lower().split()
                for palabra in palabras:
                    contactos[nombre][palabra] = contactos[nombre].get(palabra, 0) + 1

    return contactos

def generar_csv(dirección: str, palabras: list[str], diccionario_palabras: dict) -> bool:

    with open(dirección, "w", newline='', encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['contacto', 'palabra', 'frecuencia'])
        for contacto, palabras_contacto in diccionario_palabras.items():
            for palabra in palabras:
                frecuencia = palabras_contacto.get(palabra, 0)
                writer.writerow([contacto, palabra, frecuencia])
        return True

def contar_palabras_markov(dirección: str):
    contactos = {}

    with open(dirección, "r", encoding="utf-8") as chat:
        for linea in chat:
            nombre, mensaje = partir_mensaje(linea)
            if nombre and mensaje and len(mensaje) >= 2: # Lo del len() es para ignorar mensajes simples.
                if nombre not in contactos:
                    contactos[nombre] = {"palabras_iniciales": {}, "palabras": {"siguientes": {}, "ultima": {}}}

                palabras = mensaje.split()
                for i in range(len(palabras)):
                    palabra = palabras[i]

                    if i == 0: # Cuenta las veces que la palabra actual fue la primera de un mensaje.
                        contactos[nombre]["palabras_iniciales"][palabra] = contactos[nombre]["palabras_iniciales"].get(palabra, 0) + 1

                    if i < len(palabras) - 1: # Cuenta la palabra siguiente a cada palabra, hasta la penúltima.
                        if palabra not in contactos[nombre]["palabras"]["siguientes"]:
                            contactos[nombre]["palabras"]["siguientes"][palabra] = {}
                        siguiente = palabras[i + 1]
                        contactos[nombre]["palabras"]["siguientes"][palabra][siguiente] = contactos[nombre]["palabras"]["siguientes"][palabra].get(siguiente, 0) + 1

                    if i == len(palabras) - 1: # Cuenta las veces que la palabra actual fue la última.
                        contactos[nombre]["palabras"]["ultima"][palabra] = contactos[nombre]["palabras"]["ultima"].get(palabra, 0) + 1

    return contactos

def elegir_primera_palabra(diccionario_palabras_markov: dict, contacto: str) -> str:
# Consigue la lista de palabras que iniciaron un mensaje junto a su frecuencia, les asigna sus pesos y elige una.
    palabras_iniciales = diccionario_palabras_markov[contacto]["palabras_iniciales"]

    if palabras_iniciales:
        opciones = list(palabras_iniciales.keys())
        total_opciones = sum(palabras_iniciales.values())
        pesos = [palabras_iniciales[palabra] / total_opciones for palabra in opciones]
        primera_palabra = random.choices(opciones, pesos)[0]
        return primera_palabra
    else:
        return None

def elegir_palabra_siguiente(diccionario_palabras_markov: dict, contacto: str, palabra_actual: str) -> str:
    # Consigo la lista de palabras que fueron siguientes a la actual junto a su frecuencia.
    # También la frecuencia en que la palabra actual fue la última.
    palabras_siguientes = diccionario_palabras_markov[contacto]["palabras"]["siguientes"].get(palabra_actual, {})
    cantidad_ultima_palabra = diccionario_palabras_markov[contacto]["palabras"]["ultima"].get(palabra_actual, 0)

    opciones = list(palabras_siguientes.keys())
    total_opciones = sum(palabras_siguientes.values()) + cantidad_ultima_palabra

    if total_opciones == 0: # Si no llega a haber ninguna siguiente o nunca fue última, termina la oración.
        return ""

    # Acá se asignan los pesos a cada palabra siguiente, junto al peso de que la misma sea la última.
    pesos_siguientes = [palabras_siguientes.get(palabra, 0) / total_opciones for palabra in opciones]
    peso_ultima = cantidad_ultima_palabra / total_opciones
    pesos = pesos_siguientes + [peso_ultima]

    # Añado el fin de oración como posibilidad, que queda ligado al peso_ultima.
    palabra_siguiente = random.choices(opciones + [""], pesos)[0]

    return palabra_siguiente

def generar_mensaje_pseudoaleatorio(diccionario_palabras_markov: dict, contacto: str) -> str:
    mensaje = [elegir_primera_palabra(diccionario_palabras_markov, contacto)]

    while True:
        palabra_actual = mensaje[-1]
        palabra_siguiente = elegir_palabra_siguiente(diccionario_palabras_markov, contacto, palabra_actual)

        if palabra_siguiente == "":
            break

        mensaje.append(palabra_siguiente)

    return " ".join(mensaje)
