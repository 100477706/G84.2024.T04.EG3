import re

from uc3m_travel.hotel_management_exception import HotelManagementException


class Attribute:
    def __init__(self):
        self._regex_pattern = ""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, _attr_value):
        regular_expression = self._regex_pattern
        myregex = re.compile(regular_expression)
        regex_matches = myregex.fullmatch(_attr_value)
        if not regex_matches:
            raise HotelManagementException(self._error_message)
        return _attr_value

    @property
    def value(self):
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = attr_value