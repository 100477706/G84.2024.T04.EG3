"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time
from uc3m_travel.hotel_departure import HotelDeparture
from uc3m_travel.store.json_store import JsonStore
from uc3m_travel.attribute.attribute_localizer import Localizer
from uc3m_travel.attribute.attribute_idcard import IdCard
from uc3m_travel.store.json_store_check_in import JsonStoreGuestArrival
from uc3m_travel.store.json_store_check_out import JsonStoreCheckOut
from uc3m_travel.store.json_store_reservation import JsonStoreReservation



class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass


        def validate_roomkey(self, roomkey):
            """validates the roomkey format using a regex"""
            configuracion = r'^[a-fA-F0-9]{64}$'
            myregex = re.compile(configuracion)
            if not myregex.fullmatch(roomkey):
                raise HotelManagementException("Invalid room key format")
            return roomkey



        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card:str,
                             name_surname:str,
                             id_card:str,
                             phone_number:str,
                             room_type:str,
                             arrival_date: str,
                             num_days:int)->str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""

            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            HotelReservation.save_reservation(my_reservation)

            return my_reservation.localizer


        def guest_arrival(self, file_input: str)->str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival(file_input)
            HotelStay.save_roomkey(my_checkin)

            return my_checkin.room_key

        def guest_checkout(self, room_key: str)->bool:
            """manages the checkout of a guest"""
            self.validate_roomkey(room_key)
            #check that the roomkey is stored in the checkins file
            checkin_store = JsonStoreGuestArrival()

            room_key_list = checkin_store.read_input_checkin_file()

            checkout_store = JsonStoreCheckOut()

            # comprobar que esa room_key es la que me han dado
            departure_date_timestamp = checkout_store.find_in_list_checkout\
                (room_key, room_key_list)

            HotelDeparture(room_key).is_today_departure(departure_date_timestamp)


            #### HACE UN FIND ####
            file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

            my_store_reservation = JsonStore()
            room_key_list = my_store_reservation.load_json_store(file_store_checkout)

            checkout_store = JsonStoreCheckOut()

            # JsonStoreCheckOut().IsGuestOut(room_key_list, room_key)
            checkout_store.IsGuestOut(room_key_list, room_key)

            save_list = JsonStore()

            save_list.save_json_store(file_store_checkout, room_key_list)

            return True

        # def read_input_checkout_file(self, file_store):
        #     try:
        #         with open(file_store, "r", encoding="utf-8", newline="") as file:
        #             room_key_list = json.load(file)
        #     except FileNotFoundError as exception:
        #         raise HotelManagementException("Error: store checkin not found") from exception
        #     except json.JSONDecodeError as exception:
        #         raise HotelManagementException(
        #             "JSON Decode Error - Wrong JSON Format") from exception
        #     return room_key_list

        # def IsGuestOut(self, room_key_list, room_key):
        #     for checkout in room_key_list:
        #         if checkout["room_key"] == room_key:
        #             raise HotelManagementException("Guest is already out")
        #
        #     room_checkout = {"room_key": room_key,
        #                      "checkout_time": datetime.timestamp(datetime.utcnow())}
        #
        #     room_key_list.append(room_checkout)

        # def find_in_list_checkout(self, room_key, room_key_list):
        #     found = False
        #     for item in room_key_list:
        #         if room_key == item["_HotelStay__room_key"]:
        #             departure_date_timestamp = item["_HotelStay__departure"]
        #             found = True
        #     if not found:
        #         raise HotelManagementException("Error: room key not found")
        #     return departure_date_timestamp


    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance