import chats_de_whatsapp_funcionalidad
def presentar_programa():
    título = "Chats de WhatsApp, por Matías Dundic"
    print("╔" + "═" * len(título) + "╗")
    print("║" + título + "║")
    print("╚" + "═" * len(título) + "╝")

def pedir_archivo():
    while True:
        print()
        dirección = input("Por favor, ingrese la dirección del archivo de chat de WhatsApp deseado, sin comillas: ")
        if not dirección:
            print()
            print("No se ingresó nada.")
            continue

        try:
            with open(dirección, "r", encoding="utf-8"):
                return dirección
        except FileNotFoundError:
            print()
            print("La dirección que ingresó no existe. Ingrese nuevamente.")
        except OSError:
            print()
            print("La dirección que ingresó no es válida o tiene comillas. Ingrese nuevamente.")

def pedir_contacto(diccionario_palabras_markov: dict):
    contactos_lista = list(diccionario_palabras_markov.keys())

    while True:
        print()
        print("Contactos del chat:")
        for i in range(len(contactos_lista)):
            print(f"{i + 1}. {contactos_lista[i]}")
        print()
        opción = input("Ingrese el número de contacto del que quiere generar el mensaje: ")
        if not opción:
            print()
            print("No se ingresó nada.")
            continue
        if opción.isdecimal():
            opción = int(opción)
            if 1 <= opción <= len(contactos_lista):
                return contactos_lista[opción - 1]
            else:
                print()
                print("Opción no válida, ingrese nuevamente.")
        else:
            print()
            print("Ingrese el número del contacto que desea elegir.")
def contar_palabras_por_contacto(dirección: str, diccionario_palabras: dict):
    while True:
        print()
        palabras = input("Ingrese las palabras a contar entre contactos, separadas por espacios: ").lower().split()
        if not palabras:
            print()
            print("No se ingresaron palabras.")
            continue
        break

    while True:
        print()
        destino = input("Ingrese el nombre del archivo de destino para guardar el reporte: ")
        if not destino:
            print()
            print("No se ingresó nada.")
            continue
        break

    if chats_de_whatsapp_funcionalidad.generar_csv(destino, palabras, diccionario_palabras):
        print()
        print(f"Informe generado como {destino}.csv")

def menú(dirección: str):
    while True:
        print()
        print("Opciones para el chat seleccionado:")
        print("1. Contar palabras (Genera un archivo .csv)")
        print("2. Generar un mensaje pseudo-aleatorio para un contacto")
        print("3. Salir del programa")
        print()
        opción = input("Ingrese el número de opción deseada: ")
        if not opción:
            print()
            print("No se ingresó nada.")
            continue

        if opción == "1":
            diccionario_palabras = chats_de_whatsapp_funcionalidad.contar_palabras(dirección)
            contar_palabras_por_contacto(dirección, diccionario_palabras)
        elif opción == "2":
            diccionario_palabras_markov = chats_de_whatsapp_funcionalidad.contar_palabras_markov(dirección)
            contacto = pedir_contacto(diccionario_palabras_markov)
            print()
            print(f"Mensaje aleatorio generado a partir de los mensajes de {contacto}:")
            print()
            print('"' + chats_de_whatsapp_funcionalidad.generar_mensaje_pseudoaleatorio(diccionario_palabras_markov, contacto) + '"')
        elif opción == "3":
            print()
            print("Saliendo del programa...")
            quit()
        else:
            print()
            print("Opción no válida, ingrese nuevamente.")
            continue
