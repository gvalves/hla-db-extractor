from __future__ import annotations


class Cli:
    @staticmethod
    def args() -> Args:
        import argparse

        parser = argparse.ArgumentParser()

        parser.add_argument('--dat', dest='dat_file',
                            type=str, required=True)
        parser.add_argument('--imgt', dest='imgt_file',
                            type=str, required=True)
        parser.add_argument('--fasta', dest='fasta_file',
                            type=str)
        parser.add_argument('--from-imgt', dest='from_imgt_file',
                            type=str)

        parser.add_argument('--normalize', dest='normalize',
                            action='store_true')
        parser.add_argument('--use-cds', dest='use_cds',
                            action='store_true')

        parser.add_argument('--reader-strategy', dest='reader_strategy',
                            type=str, default='default')
        parser.add_argument('--writer-strategy', dest='writer_strategy',
                            type=str, default='default')
        parser.add_argument('--reader-parser-strategy', dest='reader_parser_strategy',
                            type=str, default='default')
        parser.add_argument('--writer-parser-strategy', dest='writer_parser_strategy',
                            type=str, default='default')

        return parser.parse_args()


class Args:
    dat_file: str
    imgt_file: str
    fasta_file: str
    from_imgt_file: str

    normalize: bool
    use_cds: bool

    reader_strategy: str
    writer_strategy: str
    reader_parser_strategy: str
    writer_parser_strategy: str
