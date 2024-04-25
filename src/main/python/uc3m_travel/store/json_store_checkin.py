import json

from uc3m_travel.store.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStoreGuestArrival(JsonStoreFather):
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_in.json"

    def find_reservation(self, my_localizer, store_list):
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                return item
            raise HotelManagementException("Error: localizer not found")

    def load_reservation_store(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                store_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Error: store reservation not found") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return store_list
