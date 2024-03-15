from argparse import ArgumentParser
from json import load, dump
from logging import INFO, basicConfig, getLogger
from os import path

basicConfig()
logger = getLogger("sync_token_address")
logger.setLevel(INFO)

BASE_PATH = "/Users/jormal/Documents/Repositories/AssetInfo/Assets"
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
TOKEN_PATH = "tokens/"


def run(chain: str):
    chains = [chain] if chain else CHAINS
    for chain in chains:
        token_path = path.join(BASE_PATH, chain, TOKEN_PATH)
        with open(path.join(token_path, "tokenInfo.json"), "r") as f:
            token_info = load(f)
            token_address = [token["Address"] for token in token_info["TokenList"] if "Address" in token]
            logger.info(f"token address for {chain}: {len(token_address)}")
        with open(path.join(token_path, "tokenAddrs.json"), "w") as f:
            dump(token_address, f, indent=2)
            f.write("\n")


def main():
    parser = ArgumentParser()
    parser.add_argument("--chain", type=str, default=None, required=False)
    args = parser.parse_args()
    logger.info(f"argument setting: {args}")
    if args.chain and args.chain not in CHAINS:
        raise Exception(f"Invalid chain: {args.chain}")
    run(args.chain)


if __name__ == "__main__":
    main()
