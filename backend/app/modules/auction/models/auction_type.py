from enum import Enum


class AuctionType(str, Enum):
    ENGLISH = 'english'
    BLIND = 'blind'
    SILENT = 'silent'
    DUTCH = 'dutch'
