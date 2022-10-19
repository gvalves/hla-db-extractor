import re

from operator import itemgetter
from typing import Tuple

from hla import Hla, HlaExon, HlaStrParserStrategy, StrHlaParserStrategy
from super_collections import List
from util import break_in_lines


class HlaStrParserAsImgt(HlaStrParserStrategy):
    @classmethod
    def parse(cls, hla: Hla, *args, **kwargs) -> str:
        exons_max_len, qt_exons = itemgetter(
            'exons_max_len', 'qt_exons'
        )(kwargs)

        result = f'#{hla.name}\n'

        for i in range(0, qt_exons):
            exon = hla.get_exon_by_number(i + 1)

            result += f'>EX{i + 1}\n'

            if not exon.phantom:
                exon_seq = exon.seq.upper()
            else:
                exon_seq = 'N' * exons_max_len[i]

            result += f'{break_in_lines(exon_seq, 60)}\n'

        return result


class HlaStrParserAsImgtNotEmptyExon(HlaStrParserStrategy):
    @classmethod
    def parse(cls, hla: Hla, *args, **kwargs) -> str:
        exons_max_len, qt_exons = itemgetter(
            'exons_max_len', 'qt_exons'
        )(kwargs)

        result = f'#{hla.name}\n'

        for i in range(0, qt_exons):
            exon = hla.get_exon_by_number(i + 1)

            if not exon.phantom:
                exon_seq = exon.seq.upper()
            else:
                exon_seq = 'N' * exons_max_len[i]

            if not exon_seq:
                continue

            result += f'>EX{i + 1}\n'
            result += f'{break_in_lines(exon_seq, 60)}\n'

        return result


class StrHlaParserFromDat(StrHlaParserStrategy):
    @classmethod
    def parse(cls, text: str, *args, **kwargs) -> Tuple[Hla, bool]:
        id = cls._extract_id(text)
        name = cls._extract_name(text)
        seq = cls._extract_seq(text)
        exons = cls._extract_exons(text, seq)

        valid = bool(id and name and seq and exons)

        return Hla(id, name, seq, exons), valid

    @staticmethod
    def _extract_id(text: str) -> str:
        regex = re.compile('(?<=^ID {3})\w+', re.MULTILINE)
        return regex.findall(text)[0]

    @staticmethod
    def _extract_name(text: str) -> str:
        regex = re.compile('(?<=^DE {3}).+?(?=,)', re.MULTILINE)
        return regex.findall(text)[0]

    @staticmethod
    def _extract_seq(text: str) -> str:
        regex = re.compile('(?<=\s)[atgc]{1,10}(?=\s)', re.MULTILINE)
        seq_chunks = List[str](regex.findall(text))

        try:
            if len(seq_chunks[0]) != 10:
                first_valid_seq_chunk = seq_chunks.find_index(
                    lambda seq_chunk, __, ___: len(seq_chunk) == 10
                )
                seq_chunks = seq_chunks[first_valid_seq_chunk:]
        except:
            return ''

        return ''.join(seq_chunks)

    @staticmethod
    def _extract_exons(text: str, seq: str) -> List[HlaExon]:
        exons = List[HlaExon]()
        regex = re.compile(
            '(?<=FT {3}exon {12})(\d+)\.\.(\d+)\sFT {19}.number=\"(\d+)',
            re.MULTILINE
        )
        exons_data = regex.findall(text)

        for exon_data in exons_data:
            exon_start, exon_end, exon_number = exon_data

            exon = HlaExon(range(int(exon_start) - 1, int(exon_end)))

            exon.number = exon_number
            exon.seq = seq

            exons.append(exon)

        return exons


class StrHlaParserFromFasta(StrHlaParserStrategy):
    @classmethod
    def parse(cls, text: str, *args, **kwargs) -> Tuple[Hla, bool]:
        id = cls._extract_id(text)
        name = cls._extract_name(text)
        seq = cls._extract_seq(text)

        valid = bool(id and name and seq)

        return Hla(id, name, seq, List()), valid

    @staticmethod
    def _extract_id(text: str) -> str:
        regex = re.compile('(?<=>HLA:)\w+', re.MULTILINE)
        return regex.findall(text)[0]

    @staticmethod
    def _extract_name(text: str) -> str:
        regex = re.compile('\w+\*[\w:]+', re.MULTILINE)
        return f'HLA-{regex.findall(text)[0]}'

    @staticmethod
    def _extract_seq(text: str) -> str:
        regex = re.compile('^[ATGC]+$', re.MULTILINE)
        return ''.join(regex.findall(text))


class StrHlaParserFromImgt(StrHlaParserStrategy):
    @classmethod
    def parse(cls, text: str, *args, **kwargs) -> Tuple[Hla, bool]:
        name = cls._extract_name(text)
        seq = cls._extract_seq(text)
        exons = cls._extract_exons(text)

        id = name
        valid = bool(name and seq and exons)

        return Hla(id, name, seq, exons), valid

    @staticmethod
    def _extract_name(text: str) -> str:
        regex = re.compile('(?<=^#).+$', re.MULTILINE)
        return regex.findall(text)[0]

    @staticmethod
    def _extract_seq(text: str) -> str:
        regex = re.compile('^[ATGCN]+$', re.MULTILINE)
        return ''.join(regex.findall(text))

    @staticmethod
    def _extract_exons(text: str) -> List[HlaExon]:
        exons = List[HlaExon]()

        exons_data = text.split('\n>EX')[1:]
        exon_start = 0
        exon_end = 0

        seq = ''

        for exon_data in exons_data:
            exon_data = exon_data.split('\n')

            exon_number = exon_data[0]
            exon_seq = ''.join(exon_data[1:]).replace('\n', '')
            seq += exon_seq

            exon_start = exon_end
            exon_end += len(exon_seq)

            exon = HlaExon(range(exon_start, exon_end))

            exon.number = exon_number
            exon.seq = seq

            exons.append(exon)

        return exons
