import json
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStoreFather:
    _file_name = ""
    _data_list = []
    _error_message_find = ""
    _error_message_not_find = ""
    def __init__(self):
        self.load_json_store(self._file_name)

    def load_json_store(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list

    def save_json_store(self, file_store):
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception
    def add_item_list(self, my_reservation):
        self.load_json_store(self._file_name)
        self._data_list.append(my_reservation.__dict__)
        self.save_json_store(self._file_name)

    def find_item(self, value, key):
        self.load_json_store(self._file_name)
        for item in self._data_list:
            if value == item[key]:
                raise HotelManagementException(self._error_message_find)