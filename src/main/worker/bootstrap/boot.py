import logging
import os
import sys

from dotenv import load_dotenv


def boot() -> None:
    load_dotenv(
        dotenv_path=os.path.dirname(os.path.abspath(__file__)) + "/../../../../.env"
    )
    short_link = logging.getLogger("short_link")
    short_link.setLevel(logging.INFO)
    if not short_link.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(message)s"))
        short_link.addHandler(handler)
    short_link.propagate = False
