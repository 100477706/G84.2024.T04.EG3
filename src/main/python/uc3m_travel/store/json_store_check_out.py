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



    """def add_item(self, value_to_add):
        self.load_store(self._file_name)
        self._data_list.append(value_to_add)
        self.save_store(self._file_name)"""