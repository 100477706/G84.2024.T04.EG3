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

            #leo los datos del fichero si existe , y si no existe creo una lista vacia
            #my_new_reservation = JsonStoreReservation()

            #Cargo los datos
            #my_new_reservation.load_json_store()

            #compruebo que esta reserva no esta en la lista

            #añado los datos de mi reserva a la lista , a lo que hubiera
            #my_new_reservation.add_item_list(my_reservation)

            #escribo la lista en el fichero
            #my_new_reservation.save_json_store()

            #Llamamos a Hotel Reservation
            my_new_reservation = HotelReservation
            my_new_reservation.save_reservation(my_reservation)

            return my_reservation.localizer

        # def save_reservation(self, my_reservation):
        #     my_store_reservation = JsonStoreReservation()
        #     my_store_reservation.find_item(my_reservation.localizer,
        #                                          "_HotelReservation__localizer",
        #                                          my_reservation.id_card,
        #                                          "_HotelReservation__id_card")
        #     my_store_reservation.add_item_list(my_reservation)


        def guest_arrival(self, file_input: str)->str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival(file_input)

            #Ahora lo guardo en el almacen nuevo de checkin
            # escribo el fichero Json con todos los datos
            file_store = JSON_FILES_PATH + "store_check_in.json"

            # leo los datos del fichero si existe , y si no existe creo una lista vacia
            my_store_resersvation = JsonStore()
            room_key_list = my_store_resersvation.load_json_store(file_store)

            # comprobar que no he hecho otro ckeckin antes
            self.find_in_list_checkin(my_checkin, room_key_list)

            #añado los datos de mi reserva a la lista , a lo que hubiera
            anadir_list = JsonStore()

            anadir_list.add_item_list(room_key_list, my_checkin)

            save_list = JsonStore()
            save_list.save_json_store(file_store , room_key_list)

            return my_checkin.room_key

        def find_in_list_checkin(self, my_checkin, room_key_list):
            for item in room_key_list:
                if my_checkin.room_key == item["_HotelStay__room_key"]:
                    raise HotelManagementException("ckeckin  ya realizado")

        def guest_checkout(self, room_key: str)->bool:
            """manages the checkout of a guest"""
            self.validate_roomkey(room_key)
            #check that the roomkey is stored in the checkins file
            file_store = JSON_FILES_PATH + "store_check_in.json"


            room_key_list = JsonStoreCheckOut().read_input_checkout_file(file_store)

            # comprobar que esa room_key es la que me han dado
            departure_date_timestamp = JsonStoreCheckOut().find_in_list_checkout(room_key, room_key_list)

            HotelDeparture(room_key).is_today_departure(departure_date_timestamp)

            file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

            my_store_resersvation = JsonStore()
            room_key_list = my_store_resersvation.load_json_store(file_store_checkout)

            JsonStoreCheckOut().IsGuestOut(room_key_list, room_key)

            save_list = JsonStore()

            save_list.save_json_store(file_store_checkout, room_key_list)

            return True

    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance