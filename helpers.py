import os
import platform
import re

def limpiar_pantalla():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input(" >")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto
        
def dni_valido(dni, lista):
    dni_pattern = re.compile(r"^\d{7,8}$")

    if not dni_pattern.match(dni):
        print("El DNI es inválido.")
        return False

    if any(cliente.dni == dni for cliente in lista):
        print("El DNI corresponde a un cliente ya registrado.")
        return False

    return True

