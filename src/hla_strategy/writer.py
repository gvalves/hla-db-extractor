from io import TextIOWrapper

from hla import HlaCollection, HlaCollectionWriterStrategy, HlaStrParser


class HlaCollectionWriterToImgt(HlaCollectionWriterStrategy):
    @classmethod
    def write_hla_collection(cls, file: TextIOWrapper, hla_collection: HlaCollection, parser: HlaStrParser) -> str:
        for hla in hla_collection.hlas.values():
            file.write(
                parser.parse(
                    hla,
                    exons_max_len=hla_collection.exons_max_len,
                    qt_exons=hla_collection.qt_exons
                )
            )
