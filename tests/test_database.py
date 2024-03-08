import unittest
import database as db
import copy
import helpers

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('42133953', 'Marta', 'Perez'),
            db.Cliente('48217483', 'Manolo', 'Lopez'),          
            db.Cliente('28984238', 'Ana', 'Garcia')
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('42133953')
        cliente_inexistente = db.Clientes.buscar('99999999')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        cliente = db.Clientes.crear('99999999', 'Luis', 'Gomez')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(cliente.dni, '99999999')
        self.assertEqual(cliente.nombre, 'Luis')
        self.assertEqual(cliente.apellido, 'Gomez')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('42133953'))
        cliente_modificado = db.Clientes.modificar('42133953', 'Luis', 'Perez')
        self.assertEqual(cliente_a_modificar.nombre, 'Marta')
        self.assertEqual(cliente_modificado.nombre, 'Luis')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('42133953')
        cliente_rebuscado = db.Clientes.buscar('42133953')
        self.assertEqual(cliente_borrado.dni, '42133953')
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('12345678', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48217483', db.Clientes.lista))