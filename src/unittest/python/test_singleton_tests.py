import unittest
from uc3m_travel import HotelManager
from uc3m_travel.store.reservation_json_store import StoreReservation


class MyTestCase(unittest.TestCase):
    def test_singleton1(self):
        mi_primera_instancia = HotelManager()
        mi_segunda_instancia = HotelManager()
        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)

    def test_singleton2(self):
        mi_primera_instancia = StoreReservation()
        mi_segunda_instancia = StoreReservation()
        self.assertEqual(mi_primera_instancia, mi_segunda_instancia)


if __name__ == '__main__':
    unittest.main()
