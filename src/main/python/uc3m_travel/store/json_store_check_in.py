import json

from uc3m_travel.store.json_store_father import JsonStoreFather
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStoreGuestArrival(JsonStoreFather):
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_in.json"

    def read_input_file(self, file_input):
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Error: file input not found") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list

    def read_input_data_from_file(self):
        try:
            my_localizer = self._data_list["Localizer"]
            my_id_card = self._data_list["IdCard"]
        except KeyError as exception:
            raise HotelManagementException("Error - Invalid Key in JSON") from exception
        return my_id_card, my_localizer

    def find_in_list_checkin(self, my_checkin, room_key_list):
        for item in room_key_list:
            if my_checkin.room_key == item["_HotelStay__room_key"]:
                raise HotelManagementException("ckeckin  ya realizado")

