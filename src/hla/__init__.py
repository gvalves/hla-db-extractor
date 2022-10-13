from __future__ import annotations
from typing import List


class Hla:
    def __init__(self, id: str, name: str, seq: str, exons: List[HlaExon]) -> None:
        self.__id = id
        self.__name = name
        self.__seq = seq
        self.__exons = exons

    def get_nth_exon(self, nth: int) -> HlaExon:
        for exon in self.exons:
            if exon.number == nth:
                return exon

        raise ValueError('Exon not found')

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def seq(self) -> str:
        return self.__seq

    @property
    def exons(self) -> List[HlaExon]:
        return self.__exons


class HlaExon:
    def __init__(self, range: range) -> None:
        self.__range = range
        self.__seq: str = ''
        self.__number: int

    @property
    def seq(self) -> str:
        return self.__seq

    @seq.setter
    def seq(self, seq: str):
        self.__seq = seq[self.range.start:self.range.stop]

    @property
    def range(self) -> range:
        return self.__range

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, number):
        if number > 0:
            self.__number = number

    @property
    def len(self) -> int:
        return self.range.stop - self.range.start
