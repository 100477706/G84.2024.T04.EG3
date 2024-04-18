''' Class HotelStay (GE2.2) '''
from datetime import datetime
import hashlib
import re
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attribute.attribute_idcard import IdCard


class HotelStay():
    """Class for representing hotel stays"""
    def __init__(self,
                 idcard:str,
                 localizer:str,
                 numdays:int,
                 roomtype:str):
        """constructor for HotelStay objects"""
        self.__alg = "SHA-256"
        self.__type = roomtype
        self.__idcard = IdCard(idcard).value
        self.__localizer = localizer
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + (numdays * 24 * 60 * 60)
        self.__room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + str(self.__arrival) + \
            ",departure:" + str(self.__departure) + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def id_card(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return self.__room_key

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """returns the value of the departure date"""
        self.__departure = value



    def validate_localizer(self, localizer):
        """validates the localizer format using a regex"""
        configuracion = r'^[a-fA-F0-9]{32}$'
        myregex = re.compile(configuracion)
        if not myregex.fullmatch(localizer):
            raise HotelManagementException("Invalid localizer")
        return localizer
    def validate_roomkey(self, roomkey):
        """validates the roomkey format using a regex"""
        configuracion = r'^[a-fA-F0-9]{64}$'
        myregex = re.compile(configuracion)
        if not myregex.fullmatch(roomkey):
            raise HotelManagementException("Invalid room key format")
        return roomkey