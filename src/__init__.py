from args import parse_args
from hla.fs import HlaReader, HlaWriter


def main():
    args = parse_args()

    hla_list = HlaReader.read_dat(args.dat)
    HlaWriter.save_as_imgt(args.imgt, hla_list)


if __name__ == '__main__':
    main()
