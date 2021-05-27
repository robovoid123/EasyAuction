from enum import Enum


class AuctionState(str, Enum):
    ONGOING = 'ongoing'
    ENDED = 'ended'
    CANCLED = 'cancled'
