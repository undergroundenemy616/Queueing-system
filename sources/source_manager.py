from typing import Any
from sources.source import Source
from utils.parse_config import parse_config
from utils.get_time import get_delay


class SourceManager:
    def __init__(self, source_amount=1):
        self.__source_amount = source_amount

    # Singleton
    def __new__(cls, source_amount=1) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(SourceManager, cls).__new__(cls)
        return cls.instance

    def generate_sources(self):
        sources = []
        for i in range(self.__source_amount):
            s = Source(parse_config("Source", "type"), parse_config("Source", "generation_law"), i,
                       self.__source_amount, 0)
            sources.append(s)
        return sources

    @staticmethod
    def get_order_priority(order):
        return order.get_source_number()

    def set_source_amount(self, source_amount):
        self.__source_amount = source_amount

    def get_source_amount(self):
        return self.__source_amount
