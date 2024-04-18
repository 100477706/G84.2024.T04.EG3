"""
Creado por Joaquín Pujol Carrillo in abr 2024
Universidad Carlos III de Madrid
"""
import json
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStore():
    def __init__(self):
        pass

    def load_json_store(self, file_store):
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list