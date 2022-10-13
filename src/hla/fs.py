import re
from typing import List
from hla import Hla, HlaExon


class HlaData:
    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.id: str = ''
        self.name: str = ''
        self.seq: str = ''
        self.exons: List[HlaExon] = []

    def is_valid(self) -> bool:
        return self.id and self.name and self.seq and len(self.exons) > 0

    def parse(self) -> Hla:
        return Hla(self.id, self.name, self.seq, self.exons)


class HlaReader:
    @staticmethod
    def read_dat(path: str) -> List[Hla]:
        hla_list: List[Hla] = []
        hla_data: HlaData = HlaData()
        reading_seq = False
        exon = None
        is_line_of_exon_number = False

        with (open(path, 'r')) as file:
            for line in file.readlines():
                if line.startswith('XX'):
                    continue

                if line.startswith('ID'):
                    if hla_data.is_valid():
                        hla_list.append(hla_data.parse())

                    hla_data.clear()
                    hla_data.id = re.findall('(?<=^ID {3})\w+', line)[0]

                    continue

                if line.startswith('DE') and not hla_data.name:
                    hla_data.name = re.findall('(?<=^DE {3}).+?(?=,)', line)[0]

                    continue

                if is_line_of_exon_number and exon != None:
                    exon.number = int(
                        re.findall('(?<=number=")\d+(?=")', line)[0]
                    )
                    is_line_of_exon_number = False

                    continue

                if line.startswith('FT   exon'):
                    exon_range = re.findall('\d+', line)

                    exon = HlaExon(
                        range(int(exon_range[0]) - 1, int(exon_range[1]))
                    )
                    hla_data.exons.append(exon)
                    is_line_of_exon_number = True

                    continue

                if line.startswith('SQ'):
                    reading_seq = True

                    continue

                if line.startswith('//'):
                    for exon in hla_data.exons:
                        exon.seq = hla_data.seq

                    reading_seq = False

                    continue

                if reading_seq:
                    hla_data.seq += ''.join(re.findall('[atgc]+', line))

                    continue

        return hla_list


class HlaWriter:
    @staticmethod
    def save_as_imgt(path: str, hla_list: List[Hla], fill: bool):
        def get_max_exons_len(hla_list: List[Hla]) -> List[int]:
            all_exons_len: List[List[int]] = []
            max_exons_len: List[int] = []

            for hla in hla_list:
                for exon in hla.exons:
                    try:
                        all_exons_len[exon.number - 1].append(exon.len)
                    except IndexError:
                        for _ in range(0, exon.number - len(all_exons_len)):
                            all_exons_len.append([])

                        all_exons_len[exon.number - 1].append(exon.len)

            for exons_len in all_exons_len:
                try:
                    max_exons_len.append(max(exons_len))
                except ValueError:
                    max_exons_len.append(0)

            return max_exons_len

        def separate_in_lines(text: str, line_len: int):
            text_separated: List[str] = []

            for i in range(0, len(text), line_len):
                text_separated.append(text[i:i + line_len])

            return '\n'.join(text_separated)

        with (open(path, 'w')) as file:
            max_exons_len = get_max_exons_len(hla_list)
            qt_exons = len(max_exons_len)

            for hla in hla_list:
                file.write(f'#{hla.name}\n')

                for i in range(1, qt_exons + 1):
                    file.write(f'>EX{i}\n')

                    try:
                        if fill:
                            exon_seq = f'{hla.get_nth_exon(i).seq.upper():N<{max_exons_len[i - 1]}}'
                        else:
                            exon_seq = f'{hla.get_nth_exon(i).seq.upper()}'
                    except:
                        exon_seq = 'N' * max_exons_len[i - 1]

                    file.write(f'{separate_in_lines(exon_seq, 60)}\n')
