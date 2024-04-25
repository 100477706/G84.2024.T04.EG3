"""Hotel reservation class"""
import hashlib
from datetime import datetime
import re

from freezegun import freeze_time

from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attribute.attribute_idcard import IdCard
from uc3m_travel.attribute.attribute_name_surname import NameSurname
from uc3m_travel.attribute.attribute_phone_number import PhoneNumber
from uc3m_travel.attribute.attribute_arrival_date import ArrivalDate
from uc3m_travel.attribute.attribute_room_type import RoomType
from uc3m_travel.attribute.attribute_credit_card import CreditCard
from uc3m_travel.attribute.attribute_num_days import NumDays
from uc3m_travel.attribute.attribute_localizer import Localizer
from uc3m_travel.store.json_store_checkin import JsonStoreGuestArrival
from uc3m_travel.store.json_store_reservation import JsonStoreReservation

class HotelReservation:
    """Class for representing hotel reservations"""
    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).value
        self.__id_card = IdCard(id_card).value
        justnow = datetime.utcnow()
        self.__arrival = ArrivalDate(arrival).value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = RoomType(room_type).value
        self.__num_days = NumDays(num_days).value
        self.__localizer = hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()

    def save_reservation(self, my_reservation):
        my_store_reservation = JsonStoreReservation()
        my_store_reservation.find_item(my_reservation.localizer,
                                       "_HotelReservation__localizer",
                                       my_reservation.id_card,
                                       "_HotelReservation__id_card")
        my_store_reservation.add_item_list(my_reservation)

    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @property
    def arrival(self):
        """property for getting the arrival"""
        return self.__arrival

    @property
    def room_type(self):
        """property for getting the room_type"""
        return self.__room_type

    @property
    def num_days(self):
        """property for getting the num_days"""
        return self.__num_days

    @classmethod
    def create_reservation_from_arrival(cls, my_id_card, my_localizer):
        # Validamos el IdCard
        my_id_card = IdCard(my_id_card).value

        # Validamos el localizer
        my_localizer = Localizer(my_localizer).value

        # buscar en almacen
        # file_store = JSON_FILES_PATH + "store_reservation.json"
        reservation_store = JsonStoreReservation()

        # leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
        # debe existir para hacer el checkin
        # store_list = self.load_reservation_store(file_store)

        # compruebo si esa reserva esta en el almacen
        # reservation = self.find_reservation(my_localizer, store_list)

        reservation = reservation_store.find_item(key1="_HotelReservation__localizer",
                                                  value1=my_localizer,
                                                  key2="_HotelReservation__id_card",
                                                  value2=my_id_card
                                                  )

        if reservation is None:
            raise HotelManagementException("Error: localizer not found")

        if my_id_card != reservation["_HotelReservation__id_card"]:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")

        # regenrar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(reservation[
                                                      "_HotelReservation__reservation_date"])
        with freeze_time(reservation_date):
            new_reservation = cls(credit_card_number=reservation[
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