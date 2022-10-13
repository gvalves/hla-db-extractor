from __future__ import annotations
from typing import List


class Hla:
    def __init__(self, id: str, name: str, seq: str, exons: List[HlaExon]) -> None:
        self.__id = id
        self.__name = name
        self.__seq = seq
        self.__exons = exons

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
    def len(self) -> int:
        return self.range.stop - self.range.start
