import csv
import config

class Cliente:

    def __init__(self, dni, nombre, apellido) -> None:
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self) -> str:
        return f"({self.dni}) {self.nombre} {self.apellido}"

class Clientes:
    
    lista = []

    @staticmethod
    def cargar_desde_csv():
        try:
            with open(config.DATABASE_PATH, newline='\n') as fichero:
                reader = csv.reader(fichero, delimiter=';')
                Clientes.lista = [Cliente(dni, nombre, apellido) for dni, nombre, apellido in reader]
        except FileNotFoundError:
            print("No se encontró el archivo 'clientes.csv'. Creando uno nuevo.")

    @staticmethod
    def guardar_en_csv():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow((cliente.dni, cliente.nombre, cliente.apellido))

    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
    
    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar_en_csv()
        return cliente
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        cliente = Clientes.buscar(dni)
        if cliente:
            cliente.nombre = nombre
            cliente.apellido = apellido
            Clientes.guardar_en_csv()
        return cliente
    
    @staticmethod
    def borrar(dni):
        cliente = Clientes.buscar(dni)
        if cliente:
            Clientes.lista.remove(cliente)
            Clientes.guardar_en_csv()
        return cliente

# Cargar clientes desde el archivo CSV al inicio
Clientes.cargar_desde_csv()
