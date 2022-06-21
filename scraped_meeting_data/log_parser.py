#!/usr/bin/.venv python3.10
from loguru import logger
import re


if __name__ == "__main__":
    file = "./data/address_cleaner.log"
    failed = re.findall(r"\[-]")
    regex = r"([-])([^A-Z][a-z][$A-Za-z])"

    for log in logger.parse(file, pattern=failed):
        print(log)