class Args:
    dat: str
    imgt: str


def parse_args() -> Args:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--dat', dest='dat', type=str, required=True)
    parser.add_argument('--imgt', dest='imgt', type=str, required=True)

    return parser.parse_args()
