from PIL import Image
from argparse import ArgumentParser
from glob import glob
from logging import INFO, basicConfig, getLogger
from os import makedirs, path

basicConfig()
logger = getLogger("downscale")
logger.setLevel(INFO)

BASE_PATH = path.join(path.dirname(path.realpath(__file__)), "..", "Assets/")
CHAINS = [
    "arbitrumgoerli",
    "arbitrumone",
    "arbitrumsepolia",
    "avalanche",
    "baobab",
    "base",
    "basegoerli",
    "basesepolia",
    "bifrost",
    "bifrosttest1",
    "binance",
    "bsctest",
    "ethereum",
    "fuji",
    "goerli",
    "klaytn",
    "mumbai",
    "optimism",
    "optimismgoerli",
    "polygon",
    "sepolia",
]
TOKEN_PATH = "tokens/images"
SIZES = {"256": 256, "128": 128, "32/x4": 128, "32/x2": 64, "32": 32}


def downscale(in_size: int, out_size: int, in_dir: path, out_dir: path):
    if out_size > in_size:
        raise Exception(f"Rate should be less than or equal to {in_size}: {out_size}")
    files = glob(path.join(in_dir, "*.png"))
    length = len(files)
    logger.info(f"files: {length}")
    for idx, fn in enumerate(files):
        logger.debug(f"run downscale for #{idx}/{length}")
        try:
            with Image.open(fn) as img:
                new_img = img.resize((out_size, out_size))
                out_file = path.join(out_dir, fn.split("/")[-1])
                new_img.save(out_file, "png", optimize=True)
        except Exception as e:
            logger.error(f"error occurred for {fn}: {e}")


def run(base: str, chain: str):
    targets = [size for size in SIZES if SIZES[size] <= SIZES[base]]
    chains = [chain] if chain else CHAINS
    logger.info(f"targets: {targets}")
    for chain in chains:
        image_path = path.join(BASE_PATH, chain, TOKEN_PATH)
        in_dir = path.join(image_path, base)
        logger.info(f"inner directory: {in_dir}")
        for target in targets:
            out_dir = path.join(image_path, target)
            is_exist = path.exists(out_dir)
            if not is_exist:
                makedirs(out_dir)
                logger.info(f"directory is created: {out_dir}")
            logger.info(f"outer directory: {out_dir}")
            downscale(SIZES[base], SIZES[target], in_dir, out_dir)


def main():
    parser = ArgumentParser()
    parser.add_argument("--base", type=str, default="256", required=True)
    parser.add_argument("--chain", type=str, default=None, required=False)
    args = parser.parse_args()
    logger.info(f"argument setting: {args}")
    if args.base not in SIZES:
        raise Exception(f"Invalid image target: {args.base}")
    if args.chain not in CHAINS:
        raise Exception(f"Invalid chain: {args.chain}")
    run(args.base, args.chain)


if __name__ == "__main__":
    main()
