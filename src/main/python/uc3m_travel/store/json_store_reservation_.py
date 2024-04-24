from uc3m_travel.store.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class JsonStoreReservation(JsonStoreFather):
    class __StoreReservation(JsonStoreFather):
        def __init__(self):
            self._data_list = []
            self._file_name = JSON_FILES_PATH + "store_reservation.json"

    # esto en la clase reservation_json_store
    __instance = None

    def __new__(cls):
        if not JsonStoreReservation.__instance:
            JsonStoreReservation.__instance = JsonStoreReservation.__StoreReservation()
        return JsonStoreReservation.__instance