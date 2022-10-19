from io import TextIOWrapper
import re

from hla import HlaContentReaderStrategy
from super_collections import List


class HlaContentReaderFromDat(HlaContentReaderStrategy):
    @classmethod
    def get_hla_content(cls, file: TextIOWrapper) -> str:
        hla_content = ''
        last_file_pos = -1
        has_to_read = False

        while file.tell() != last_file_pos:
            last_file_pos = file.tell()
            line = file.readline()

            if line.startswith('ID'):
                has_to_read = True

            if line.startswith('//'):
                break

            if has_to_read:
                hla_content += line

        return hla_content


class HlaContentReaderFromFasta(HlaContentReaderStrategy):
    @classmethod
    def get_hla_content(cls, file: TextIOWrapper) -> str:
        hla_content = ''
        last_file_pos = -1
        has_to_read = False

        while file.tell() != last_file_pos:
            last_file_pos = file.tell()
            line = file.readline()

            if line.startswith('>'):
                if has_to_read:
                    break

                has_to_read = True

            if has_to_read:
                hla_content += line

        return hla_content


class HlaContentReaderQuickFromDat(HlaContentReaderStrategy):
    __hlas_contents = None

    @classmethod
    def get_hla_content(cls, file: TextIOWrapper) -> str:
        regex = re.compile('\n//\n?', re.MULTILINE)

        if not cls.__hlas_contents:
            try:
                cls.__hlas_contents = iter(regex.split(file.read()))
            except:
                return ''

        try:
            return next(cls.__hlas_contents)
        except:
            return ''


class HlaContentReaderFromImgt(HlaContentReaderStrategy):
    @classmethod
    def get_hla_content(cls, file: TextIOWrapper) -> str:
        hla_content = ''
        last_file_pos = -1
        has_to_read = False

        while file.tell() != last_file_pos:
            last_file_pos = file.tell()
            line = file.readline()

            if line.startswith('#'):
                if has_to_read:
                    break

                has_to_read = True

            if has_to_read:
                hla_content += line

        return hla_content
