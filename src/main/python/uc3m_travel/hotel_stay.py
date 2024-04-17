''' Class HotelStay (GE2.2) '''
from datetime import datetime
import hashlib
import re
from uc3m_travel.hotel_management_exception import HotelManagementException


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
        self.__idcard = idcard
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


    def validate_idcard(self, my_id_card):
        configuracion = r'^[0-9]{8}[A-Z]{1}$'
        my_regex = re.compile(configuracion)
        if not my_regex.fullmatch(my_id_card):
            raise HotelManagementException("Invalid IdCard format")
        if not self.validate_dni(my_id_card):
            raise HotelManagementException("Invalid IdCard letter")
        return my_id_card
    @staticmethod
    def validate_dni(dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        characters = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                      "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                      "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                      "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        digits = int(dni[0:8])
        letter = str(digits % 23)
        return dni[8] == characters[letter]

    def validate_localizer(self, localizer):
        """validates the localizer format using a regex"""
        configuracion = r'^[a-fA-F0-9]{32}$'
        myregex = re.compile(configuracion)
        if not myregex.fullmatch(localizer):
            raise HotelManagementException("Invalid localizer")
        return localizer