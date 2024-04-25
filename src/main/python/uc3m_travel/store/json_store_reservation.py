from uc3m_travel.store.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class JsonStoreReservation(JsonStoreFather):
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_reservation.json"
    _error_message_find = "Reservation already exists"

    def find_item(self, value1, key1, value2, key2):
        self.load_json_store(self._file_name)
        super().find_item_general(value1, key1)
        self._error_message_find = "This ID card has another reservation"
        super().find_item_general(value2, key2)