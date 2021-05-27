from enum import Enum


class Conditions(str, Enum):
    BRAND_NEW = 'brandnew'
    BEST = 'best'
    GOOD = 'good'
    POOR = 'poor'
