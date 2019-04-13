from enum import Enum


class Events(Enum):
    """
    List of events
    - good_guy_entering = 1
    - bad_guy_entering = 2
    - leaving_house = 3
    - requesting_dance_mode = 4
    - requesting_romantic_mode = 5
    """
    good_guy_entering = 1
    bad_guy_entering = 2
    leaving_house = 3
    requesting_dance_mode = 4
    requesting_romantic_mode = 5
