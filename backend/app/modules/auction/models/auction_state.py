from enum import Enum


class AuctionState(str, Enum):
    CREATED = 'created'
    ONGOING = 'ongoing'
    ENDED = 'ended'
    CANCLED = 'cancled'
