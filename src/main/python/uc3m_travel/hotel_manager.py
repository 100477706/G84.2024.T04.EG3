"""Module for the hotel manager"""
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from uc3m_travel.hotel_departure import HotelDeparture


class HotelManager:
    # pylint: disable = C0103
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass

        # pylint: disable=too-many-arguments
        @staticmethod
        def room_reservation(
                             credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:
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

        @staticmethod
        def guest_arrival(file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival(file_input)
            HotelStay.save_roomkey(my_checkin)

            return my_checkin.room_key

        @staticmethod
        def guest_checkout(room_key: str) -> bool:
            """manages the checkout of a guest"""
            HotelDeparture.search_room_key_for_client(room_key)
            HotelDeparture.departure_for_client(room_key)

            return True

    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance
