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
from uc3m_travel.store.json_store_checkin import JsonStoreGuestArrival
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
            my_new_reservation.save_reservation(self, my_reservation)

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
            input_list = self.read_input_file(file_input)

            # comprobar valores del fichero
            my_id_card, my_localizer = self.read_input_data_from_file(input_list)

            new_reservation = self.create_reservation_from_arrival(my_id_card, my_localizer)

            # compruebo si hoy es la fecha de checkin
            reservation_format = "%d/%m/%Y"
            date_obj = datetime.strptime(new_reservation.arrival, reservation_format)
            if date_obj.date()!= datetime.date(datetime.utcnow()):
                raise HotelManagementException("Error: today is not reservation date")

            # genero la room key para ello llamo a Hotel Stay
            my_checkin = HotelStay(idcard=my_id_card, numdays=int(new_reservation.num_days),
                                   localizer=my_localizer, roomtype=new_reservation.room_type)

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

        def create_reservation_from_arrival(self, my_id_card, my_localizer):
            # Validamos el IdCard
            my_id_card = IdCard(my_id_card).value

            # Validamos el localizer
            my_localizer = Localizer(my_localizer).value

            # buscar en almacen
            file_store = JSON_FILES_PATH + "store_reservation.json"

            # leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
            # debe existir para hacer el checkin
            store_list = self.load_reservation_store(file_store)

            # compruebo si esa reserva esta en el almacen
            reservation = self.find_reservation(my_localizer, store_list)

            if my_id_card != reservation["_HotelReservation__id_card"]:
                raise HotelManagementException("Error: Localizer is not correct for this IdCard")

            # regenrar clave y ver si coincide
            reservation_date = datetime.fromtimestamp(reservation[
                                                          "_HotelReservation__reservation_date"])

            with freeze_time(reservation_date):
                new_reservation = HotelReservation(credit_card_number=reservation[
                    "_HotelReservation__credit_card_number"],
                                                   id_card=reservation[
                                                       "_HotelReservation__id_card"],
                                                   num_days=reservation[
                                                       "_HotelReservation__num_days"],
                                                   room_type=reservation[
                                                       "_HotelReservation__room_type"],
                                                   arrival=reservation[
                                                       "_HotelReservation__arrival"],
                                                   name_surname=reservation[
                                                       "_HotelReservation__name_surname"],
                                                   phone_number=reservation[
                                                       "_HotelReservation__phone_number"])
            if new_reservation.localizer != my_localizer:
                raise HotelManagementException("Error: reservation has been manipulated")
            return new_reservation

        def read_input_data_from_file(self, input_list):
            try:
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as exception:
                raise HotelManagementException("Error - Invalid Key in JSON") from exception
            return my_id_card, my_localizer

        def find_in_list_checkin(self, my_checkin, room_key_list):
            for item in room_key_list:
                if my_checkin.room_key == item["_HotelStay__room_key"]:
                    raise HotelManagementException("ckeckin  ya realizado")

        def find_reservation(self, my_localizer, store_list):
            for item in store_list:
                if my_localizer == item["_HotelReservation__localizer"]:
                    return item
                raise HotelManagementException("Error: localizer not found")

        def load_reservation_store(self, file_store):
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    store_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store reservation not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return store_list

        def read_input_file(self, file_input):
            try:
                with open(file_input, "r", encoding="utf-8", newline="") as file:
                    input_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: file input not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return input_list




        def guest_checkout(self, room_key: str)->bool:
            """manages the checkout of a guest"""
            self.validate_roomkey(room_key)
            #check that the roomkey is stored in the checkins file
            file_store = JsonStoreGuestArrival()._file_name


            room_key_list = self.read_input_checkout_file(file_store)

            # comprobar que esa room_key es la que me han dado
            departure_date_timestamp = self.find_in_list_checkout(room_key, room_key_list)

            HotelDeparture(room_key).is_today_departure(departure_date_timestamp)

            file_store_checkout = JSON_FILES_PATH + "store_check_out.json"

            my_store_resersvation = JsonStore()
            room_key_list = my_store_resersvation.load_json_store(file_store_checkout)

            for checkout in room_key_list:
                if checkout["room_key"] == room_key:
                    raise HotelManagementException("Guest is already out")

            room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

            room_key_list.append(room_checkout)

            save_list = JsonStore()

            save_list.save_json_store(file_store_checkout, room_key_list)

            return True

        def find_in_list_checkout(self, room_key, room_key_list):
            found = False
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp = item["_HotelStay__departure"]
                    found = True
            if not found:
                raise HotelManagementException("Error: room key not found")
            return departure_date_timestamp

        def read_input_checkout_file(self, file_store):
            try:
                with open(file_store, "r", encoding="utf-8", newline="") as file:
                    room_key_list = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Error: store checkin not found") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return room_key_list

    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance