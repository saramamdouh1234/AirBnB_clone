#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place"""

    city_id = ""
    user_id = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    name = ""
    description = ""
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
