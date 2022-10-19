from __future__ import annotations

from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Tuple

from super_collections import Dict, List, Set


class HlaReader:
    def __init__(self, strategy: HlaContentReaderStrategy, parser: StrHlaParser) -> None:
        self.__strategy = strategy
        self.__parser = parser

    def read(self, path: str) -> Set[HlaCollection]:
        hla_collections = Set[HlaCollection]()

        with (open(path, 'r')) as file:
            while True:
                hla_content = self.get_hla_content(file)

                if not hla_content:
                    break

                hla, valid = self.parser.parse(hla_content)

                if not valid:
                    continue

                hla_collection = HlaCollection(hla.type)
                hla_collection = hla_collections.add(hla_collection)
                hla_collection.add(hla)

        return hla_collections

    def get_hla_content(self, file: TextIOWrapper) -> str:
        return self.strategy.get_hla_content(file)

    @property
    def strategy(self) -> HlaContentReaderStrategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: HlaContentReaderStrategy):
        self.__strategy = strategy

    @property
    def parser(self) -> StrHlaParser:
        return self.__parser

    @parser.setter
    def parser(self, parser: StrHlaParser):
        self.__parser = parser


class HlaContentReaderStrategy(ABC):
    @classmethod
    @abstractmethod
    def get_hla_content(cls, file: TextIOWrapper) -> str:
        pass


class HlaWriter:
    def __init__(self, strategy: HlaCollectionWriterStrategy, parser: HlaStrParser) -> None:
        self.__strategy = strategy
        self.__parser = parser

    def write(self, path: str, hla_collections: Set[HlaCollection]):
        with (open(path, 'w')) as file:
            for hla_collection in hla_collections:
                self.strategy.write_hla_collection(
                    file,
                    hla_collection,
                    self.parser
                )

    @property
    def strategy(self) -> HlaCollectionWriterStrategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: HlaCollectionWriterStrategy):
        self.__strategy = strategy

    @property
    def parser(self) -> HlaStrParser:
        return self.__parser

    @parser.setter
    def parser(self, parser: HlaStrParser):
        self.__parser = parser


class HlaCollectionWriterStrategy(ABC):
    @classmethod
    @abstractmethod
    def write_hla_collection(cls, file: TextIOWrapper, hla_collection: HlaCollection, parser: HlaStrParser) -> str:
        pass


class StrHlaParser:
    def __init__(self, strategy: StrHlaParserStrategy) -> None:
        self.__strategy = strategy

    def parse(self, text: str, *args, **kwargs) -> Tuple[Hla, bool]:
        return self.strategy.parse(text, *args, **kwargs)

    @property
    def strategy(self) -> StrHlaParserStrategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: StrHlaParserStrategy):
        self.__strategy = strategy


class StrHlaParserStrategy(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, text: str, *args, **kwargs) -> Tuple[Hla, bool]:
        pass


class HlaStrParser:
    def __init__(self, strategy: HlaStrParserStrategy) -> None:
        self.__strategy = strategy

    def parse(self, hla: Hla, *args, **kwargs) -> str:
        return self.strategy.parse(hla, *args, **kwargs)

    @property
    def strategy(self) -> HlaStrParserStrategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: HlaStrParserStrategy):
        self.__strategy = strategy


class HlaStrParserStrategy(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, hla: Hla, *args, **kwargs) -> str:
        pass


class HlaCollection:
    def __init__(self, type: str) -> None:
        self.__type = type
        self.__hlas = Dict[Hla]()
        self.__exons_max_len = List[int]()
        self.__qt_exons = 0

    def __eq__(self, other: HlaCollection) -> bool:
        self_type = self.type
        other_type = other.type

        return self_type == other_type

    def __hash__(self) -> int:
        return hash(self.type)

    def add(self, hla: Hla):
        exons = hla.exons_full
        qt_exons = hla.last_exon_number

        self.__hlas[hla.id] = hla

        if self.qt_exons == 0:
            self.__qt_exons = qt_exons

            for exon in exons:
                self.__exons_max_len.append(exon.len)

            return

        self.__qt_exons = max(self.qt_exons, qt_exons)

        for i in range(0, self.qt_exons):
            try:
                new_exon_len = exons[i].len
            except IndexError:
                break

            try:
                old_exon_len = self.__exons_max_len[i]
            except IndexError:
                self.__exons_max_len.append(new_exon_len)
                continue

            if new_exon_len > old_exon_len:
                self.__exons_max_len[i] = new_exon_len

    def config_exons_ranges_for_cds(self):
        for hla in self.__hlas.values():
            hla.config_exons_ranges_for_cds()

    def restore_exons_ranges(self):
        for hla in self.__hlas.values():
            hla.restore_exons_ranges()

    @property
    def type(self) -> str:
        return self.__type

    @property
    def hlas(self) -> Dict[Hla]:
        return self.__hlas

    @property
    def exons_max_len(self) -> List[int]:
        return self.__exons_max_len

    @property
    def qt_exons(self) -> int:
        return self.__qt_exons


class Hla:
    def __init__(self, id: str, name: str, seq: str, exons: List[HlaExon]) -> None:
        self.__id = id
        self.__name = name
        self.__seq = seq
        self.__exons = exons
        self.__exons_ranges = List[range]()

    def get_exon_by_number(self, number: int) -> HlaExon:
        exon = self.__exons.find(lambda exon, __, ___: exon.number == number)
        return exon if exon else HlaExon.create_phantom()

    def add_exon(self, exon: HlaExon):
        self.__exons.append(exon)
        self.__exons_ranges.append(exon.range)

    def update_exons_seq(self, seq: str):
        for exon in self.__exons:
            exon.seq = seq

    def config_exons_ranges_for_cds(self):
        start = 0

        for exon in self.__exons:
            stop = start + exon.len
            exon.range = range(start, stop)
            start = stop

    def restore_exons_ranges(self):
        for i, exon in enumerate(self.__exons):
            exon.range = self.__exons_ranges[i]

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

    @property
    def type(self) -> str:
        return self.name.split('*')[0]

    @property
    def last_exon_number(self) -> int:
        try:
            return max([exon.number for exon in self.__exons])
        except:
            return 0

    @property
    def exons_full(self) -> List[HlaExon]:
        return [self.get_exon_by_number(i) for i in range(1, self.last_exon_number + 1)]


class HlaExon:
    def __init__(self, range: range) -> None:
        self.range = range
        self.__seq = ''
        self.__number = 0
        self.__phantom = False

    def __setattr__(self, name: str, value) -> None:
        try:
            phantom = self.__phantom
        except:
            phantom = False

        if not phantom:
            object.__setattr__(self, name, value)

    @classmethod
    def create_phantom(cls) -> HlaExon:
        exon = cls(range(0, 0))
        setattr(exon, f'_{cls.__name__}__phantom', True)
        return exon

    @property
    def seq(self) -> str:
        return self.__seq

    @seq.setter
    def seq(self, seq: str):
        start = self.range.start
        stop = self.range.stop
        self.__seq = seq[start:stop]

    @property
    def range(self) -> range:
        return self.__range

    @range.setter
    def range(self, new_range: range):
        start = max(0, new_range.start)
        stop = max(start, new_range.stop)
        self.__range = range(start, stop)

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, number):
        number = int(number)
        if number > 0:
            self.__number = number

    @property
    def phantom(self) -> bool:
        return self.__phantom

    @property
    def len(self) -> int:
        return self.range.stop - self.range.start
