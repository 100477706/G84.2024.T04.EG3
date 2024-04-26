from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.store.json_store_check_in import JsonStoreGuestArrival
from uc3m_travel.store.json_store_check_out import JsonStoreCheckOut
from uc3m_travel.attribute.attribute_room_key import RoomKey

class HotelDeparture:
    def __init__(self, room_key):
        self.__room_key = room_key
        self.__checkout_time = datetime.timestamp(datetime.utcnow())

    @property
    def room_key(self):
        """Property that represents the product_id of the patient"""
        return self.__room_key

    @room_key.setter
    def room_key(self, value):
        self.__room_key = value

    # Comprueba si hoy es el día de salida
    def is_today_departure(self, departure_date_timestamp):
        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")

    @classmethod
    def search_room_key_for_client(self, room_key):
        # check that the roomkey is stored in the checkins file
        checkin_store = JsonStoreGuestArrival()
        room_key_list = checkin_store.read_input_checkin_file()
        checkout_store = JsonStoreCheckOut()
        # comprobar que esa room_key es la que me han dado
        departure_date_timestamp = checkout_store.find_in_list_checkout \
            (room_key, room_key_list)
        HotelDeparture(room_key).is_today_departure(departure_date_timestamp)