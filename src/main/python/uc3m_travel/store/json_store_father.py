import json
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStoreFather:

    def __init__(self):
        self._file_name = ""
        self._data_list = []

    def load_json_store(self):
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list
    def find_item_in_store(self, my_reservation):
        for item in self._data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")

    def save_json_store(self, room_key_list):
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(room_key_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception
    def add_item_list(self, data_list, my_reservation):
        data_list.append(my_reservation.__dict__)

