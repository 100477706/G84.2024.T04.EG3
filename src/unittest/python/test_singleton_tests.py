import unittest
from uc3m_travel import HotelManager
from uc3m_travel.store.json_store_reservation import JsonStoreReservation
## CUIDADO QUE APARECE EL BACKUP PORQUE HAY UNA FALLITA CON EL SINGLETON DE HOTEL RESERVATION

class MyTestCase(unittest.TestCase):
    def test_singleton1(self):
        mi_primera_instancia = HotelManager()
        mi_segunda_instancia = HotelManager()
        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)

    def test_singleton2(self):
        mi_primera_instancia = JsonStoreReservation()
        mi_segunda_instancia = JsonStoreReservation()
        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)


if __name__ == '__main__':
    unittest.main()
