from datetime import datetime

from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.json_store_father import JsonStoreFather

class JsonStoreCheckOut(JsonStoreFather):
    class __JsonStoreCheckOut(JsonStoreFather):
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

    __instance = None
    def __new__(cls):
        if not JsonStoreCheckOut.__instance:
            JsonStoreCheckOut.__instance = JsonStoreCheckOut.__JsonStoreCheckOut()
        return JsonStoreCheckOut.__instance