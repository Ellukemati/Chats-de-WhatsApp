import chats_de_whatsapp_interfaz

def main():
    chats_de_whatsapp_interfaz.presentar_programa()

    archivo = chats_de_whatsapp_interfaz.pedir_archivo()

    chats_de_whatsapp_interfaz.menú(archivo)

main()
