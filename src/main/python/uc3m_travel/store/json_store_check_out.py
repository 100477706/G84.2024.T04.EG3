import json
from datetime import datetime

from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.json_store_father import JsonStoreFather

class JsonStoreCheckOut(JsonStoreFather):
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_out_.json"
    _error_message_find = "Guest is already out"

    def IsGuestOut(self, room_key_list,room_key):
        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException(self._error_message_find)

        room_checkout = {"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

        room_key_list.append(room_checkout)

    def find_in_list_checkout(self, room_key, room_key_list):
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")
        return departure_date_timestamp

    def read_input_checkout_file(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Error: store checkin not found") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return room_key_list



    """def add_item(self, value_to_add):
        self.load_store(self._file_name)
        self._data_list.append(value_to_add)
        self.save_store(self._file_name)"""