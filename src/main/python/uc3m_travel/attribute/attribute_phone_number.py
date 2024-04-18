from uc3m_travel.attribute.attribute import Attribute
from uc3m_travel import HotelManagementException
import re

class PhoneNumber(Attribute):
    def __init__(self, attr_value):
        self.__regex_pattern = r"^(\+)[0-9]{9}"
        self.__error_message = "Invalid name format"
        self.__attr_value = self._validate(attr_value)