import json

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class JsonStoreReservation(JsonStoreFather):
    class __JsonStoreReservation(JsonStoreFather):
        _data_list = []
        _file_name = JSON_FILES_PATH + "store_reservation.json"
        _error_message_find = ""

        def find_item(self, value1, key1, value2, key2):
            self.load_json_store(self._file_name)
            self._error_message_find = "Reservation already exists"
            super().find_item(value1, key1)
            self._error_message_find = "This ID card has another reservation"
            super().find_item(value2, key2)

        def load_reservation_store(self):
            try:
                with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                    self._data_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store reservation not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException(
                    "JSON Decode Error - Wrong JSON Format") from exception
            return self._data_list


    # esto en la clase reservation_json_store
    __instance = None

    def __new__(cls):
        if not JsonStoreReservation.__instance:
            JsonStoreReservation.__instance = JsonStoreReservation.__JsonStoreReservation()
        return JsonStoreReservation.__instance