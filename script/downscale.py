
from argparse import ArgumentParser
from glob import glob
from logging import INFO, basicConfig, getLogger
from os import makedirs, path
from re import I

from PIL import Image

basicConfig()
logger = getLogger("downscale")
logger.setLevel(INFO)

BASE_PATH = "/Users/jormal/Documents/Repositories/AssetInfo/Assets"
CHAINS = [
    "arbitrumgoerli",
    "arbitrumone",
    "avalanche",
    "baobab",
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
]
TOKEN_PATH = "tokens/images"
SIZES = {
    "256": 256,
    "128": 128,
    "32/x4": 128,
    "32/x2": 64,
    "32": 32
}


def downscale (in_size: int, out_size: int, in_dir: path, out_dir: path):
    if out_size > in_size: raise Exception(f"Rate should be less than or equal to {in_size}: {out_size}")
    files = glob(path.join(in_dir, "*.png"))
    length = len(files)
    logger.info(f"files: {length}")
    for idx, fn in enumerate(files):
        logger.debug(f"run downscale for #{idx}/{length}")
        try:
            with Image.open(fn) as img:
                new_img = img.resize((out_size, out_size))
                out_file = path.join(out_dir, fn.split("/")[-1])
                new_img.save(out_file, "png")
        except Exception as e:
            logger.error(f"error occurred for {fn}: {e}")

def run(base: str):
    targets = [ size for size in SIZES if size != base and SIZES[size] <= SIZES[base]]
    logger.info(f"targets: {targets}")
    for chain in CHAINS:
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
            rate = int(SIZES[base] / SIZES[target])
            logger.info(f"downscale rate: {rate}")
            downscale(SIZES[base], SIZES[target], in_dir, out_dir)

def main():
    parser = ArgumentParser()
    parser.add_argument("--base", type=str, default="256", required=True)
    args = parser.parse_args()
    logger.info(f"argument setting: {args}")
    if args.base not in SIZES: raise Exception(f"Invalid image target: {args.base}")
    run(args.base)

if __name__ == "__main__":
    main()
