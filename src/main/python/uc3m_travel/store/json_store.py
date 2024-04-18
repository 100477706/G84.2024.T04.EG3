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
    def find_item_in_store(self, data_list, my_reservation):
        for item in data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")

    def save_json_store(self, file_store_checkout, room_key_list):
        try:
            with open(file_store_checkout, "w", encoding="utf-8", newline="") as file:
                json.dump(room_key_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception
    def add_item_list(self, data_list, my_reservation):
        data_list.append(my_reservation.__dict__)

