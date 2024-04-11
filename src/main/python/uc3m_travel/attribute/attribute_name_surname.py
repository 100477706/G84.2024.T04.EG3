from uc3m_travel.attribute.attribute import Attribute
from uc3m_travel import HotelManagementException

class NameSurname(Attribute):
    def __init__(self, attr_value):
        self.__regex_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self.__error_message = "Invalid name format"
        self.__attr_value = self._validate(attr_value)

    def validate_name_surname(self, guest_name):
        r = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        myregex = re.compile(r)
        regex_matches = myregex.fullmatch(guest_name)
        if not regex_matches:
            raise HotelManagementException("Invalid name format")
        return guest_name