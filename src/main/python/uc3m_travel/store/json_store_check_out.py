"""
Creado por Joaquín Pujol Carrillo in abr 2024
Universidad Carlos III de Madrid
"""
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from json_store import JsonStore

class JsonStoreCheckOut(JsonStore):
    _data_list = []
    _file_name = JSON_FILES_PATH + "store_check_out_.json"
    _error_message_find = "Guest is already out"

    """def add_item(self, value_to_add):
        self.load_store(self._file_name)
        self._data_list.append(value_to_add)
        self.save_store(self._file_name)"""