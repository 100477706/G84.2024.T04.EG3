"""
Creado por Joaquín Pujol Carrillo in abr 2024
Universidad Carlos III de Madrid
"""
from datetime import datetime

class HotelDeparture:
    def __init__(self, room_key):
        self.__room_key = room_key
        self.__checkout_time = datetime.timestamp(datetime.utcnow())
