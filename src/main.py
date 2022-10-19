from cli import Cli
from hla import HlaReader, HlaStrParser, HlaWriter, StrHlaParser

from hla_strategy.parser \
    import (HlaStrParserAsImgt, HlaStrParserAsImgtNotEmptyExon,
            StrHlaParserFromDat, StrHlaParserFromFasta, StrHlaParserFromImgt)

from hla_strategy.reader \
    import (HlaContentReaderFromDat, HlaContentReaderFromFasta,
            HlaContentReaderFromImgt, HlaContentReaderQuickFromDat)

from hla_strategy.writer import HlaCollectionWriterToImgt
from super_collections import List


reader_strategies = {
    'default': HlaContentReaderFromDat,
    'quick': HlaContentReaderQuickFromDat
}
writer_strategies = {
    'default': HlaCollectionWriterToImgt
}
reader_parser_strategies = {
    'default': StrHlaParserFromDat
}
writer_parser_strategies = {
    'default': HlaStrParserAsImgt,
    'remove_empty_exon': HlaStrParserAsImgtNotEmptyExon
}

hlascan_types = List[str](['HLA-A', 'HLA-B', 'HLA-C', 'HLA-E', 'HLA-F', 'HLA-G',
                           'MICA', 'MICB', 'HLA-DMA', 'HLA-DMB', 'HLA-DOA',
                           'HLA-DOB', 'HLA-DPA1', 'HLA-DPB1', 'HLA-DQA1', 'HLA-DQB1',
                           'HLA-DRA', 'HLA-DRB1', 'HLA-DRB5', 'TAP1', 'TAP2'
                           ])


def main():
    args = Cli.args()

    dat_file = args.dat_file
    imgt_file = args.imgt_file
    fasta_file = args.fasta_file
    from_imgt_file = args.from_imgt_file
    normalize = args.normalize
    use_cds = args.use_cds
    reader_strategy = args.reader_strategy
    writer_strategy = args.writer_strategy
    reader_parser_strategy = args.reader_parser_strategy
    writer_parser_strategy = args.writer_parser_strategy

    reader_parser_strategy = reader_parser_strategies.get(
        reader_parser_strategy
    )

    writer_parser_strategy = writer_parser_strategies.get(
        writer_parser_strategy
    )

    reader_strategy = reader_strategies.get(
        reader_strategy
    )

    writer_strategy = writer_strategies.get(
        writer_strategy
    )

    if not reader_parser_strategy:
        print('Invalid reader parser strategy')
        exit(1)

    if not writer_parser_strategy:
        print('Invalid writer parser strategy')
        exit(1)

    if not reader_strategy:
        print('Invalid reader strategy')
        exit(1)

    if not writer_strategy:
        print('Invalid writer strategy')
        exit(1)

    reader_parser = StrHlaParser(reader_parser_strategy)
    writer_parser = HlaStrParser(writer_parser_strategy)

    reader = HlaReader(reader_strategy, reader_parser)
    writer = HlaWriter(writer_strategy, writer_parser)

    hla_collections = reader.read(dat_file)

    if use_cds:
        for hc in hla_collections:
            hc.config_exons_ranges_for_cds()

    if fasta_file:
        reader = HlaReader(HlaContentReaderFromFasta, StrHlaParserFromFasta)
        fas_hla_collections = reader.read(fasta_file)

        fas_hla_collections = fas_hla_collections.to_dict(lambda hc: hc.type)

        for hc in hla_collections:
            imgt_hc = fas_hla_collections.get(hc.type)

            if not imgt_hc:
                continue

            for hla in hc.hlas.values():
                imgt_hla = imgt_hc.hlas.get(hla.id)

                if not imgt_hla:
                    continue

                for exon in hla.exons:
                    exon.seq = imgt_hla.seq

    if from_imgt_file:
        reader = HlaReader(HlaContentReaderFromImgt, StrHlaParserFromImgt)
        imgt_hla_collections = reader.read(from_imgt_file)

        imgt_hla_collections = imgt_hla_collections.to_dict(lambda hc: hc.type)

        for hc in hla_collections:
            imgt_hc = imgt_hla_collections.get(hc.type)

            if not imgt_hc:
                continue

            for hla in hc.hlas.copy().values():
                imgt_hla = imgt_hc.hlas.get(hla.name)

                if not imgt_hla:
                    continue

                hc.hlas[hla.id] = imgt_hla

    writer.write(imgt_file, hla_collections.filter(
        lambda hc, __, ___: hlascan_types.contains(hc.type)
    ))


if __name__ == '__main__':
    main()
