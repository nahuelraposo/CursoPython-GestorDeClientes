import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()

        print("=====================================")
        print("       Bienvenido al Gestor          ")
        print("=====================================")
        print("[1] - Listar los clientes            ")
        print("[2] - Buscar un cliente              ")
        print("[3] - Agregar un cliente             ")
        print("[4] - Modificar un cliente           ")
        print("[5] - Borrar un cliente              ")
        print("[6] - Cerrar el gestor               ")

        opcion = input("Seleccione una opción: ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            listar_clientes()
        elif opcion == '2':
            buscar_cliente()
        elif opcion == '3':
            agregar_cliente()
        elif opcion == '4':
            modificar_cliente()
        elif opcion == '5':
            borrar_cliente()
        elif opcion == '6':
            print("Cerrando gestor...\n")
            break
        else:
            print("Error: Opción inválida.")

        input("\nPresione Enter para continuar...")


def listar_clientes():
    print("Listando clientes...\n")
    for cliente in db.Clientes.lista:
        print(cliente)

def buscar_cliente():
    print("Buscando cliente...\n")
    dni = helpers.leer_texto(7, 8, "DNI: ").upper()
    cliente = db.Clientes.buscar(dni)
    if cliente:
        print(cliente)
    else:
        print("Cliente no encontrado.")

def agregar_cliente():
    print("Agregando cliente...\n")
    dni = None
    while(True):
        dni = helpers.leer_texto(7, 8, "DNI: ").upper()
        if helpers.dni_valido(dni, db.Clientes.lista):
            nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 caracteres): ").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 caracteres): ").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente agregado correctamente.")
            break

def modificar_cliente():
    print("Modificando cliente...\n")
    dni = helpers.leer_texto(7, 8, "DNI: ").upper()
    cliente = db.Clientes.buscar(dni)
    if cliente:
        nombre = helpers.leer_texto(2, 30, "Nombre (de 2 a 30 caracteres): ").capitalize()
        apellido = helpers.leer_texto(2, 30, "Apellido (de 2 a 30 caracteres): ").capitalize()
        db.Clientes.modificar(dni, nombre, apellido)
        print("Cliente modificado correctamente.")
    else:
        print("Cliente no encontrado.")

def borrar_cliente():
    print("Borrando cliente...\n")
    dni = helpers.leer_texto(7, 8, "DNI: ").upper()
    cliente = db.Clientes.buscar(dni)
    if cliente:
        db.Clientes.borrar(dni)
        print("Cliente borrado correctamente.")
    else:
        print("Cliente no encontrado.")