"""Singleton for tempdir."""

import tempfile
from loguru import logger

tempdir = tempfile.TemporaryDirectory()
tempdir_name = tempdir.name

if __name__ == "__main__":
    logger.info(f"tempdir_name: {tempdir_name}")
