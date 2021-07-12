from io import BytesIO
import math
from loguru import logger
from typing import List

from .factory import create_writer, create_reader
from .utils import basedir_exists, get_files_from_dir, get_filename


def split_pdf_batch(file, batch=30):
    inputpdf = create_reader(file)

    total_pages = inputpdf.numPages
    no_of_batch = math.ceil(total_pages // batch)
    offset = 0

    while no_of_batch >= 0:
        output = create_writer()

        for i in range(batch):
            page = i + offset
            if page < total_pages:
                output.addPage(inputpdf.getPage(page))

        low = offset
        high = offset + batch

        yield low, high, output

        offset += batch
        no_of_batch -= 1


def split_pdf_range(file: str, split_range: List[int]):
    """
    Extract/Split `file` from pages
    split_range[0] to split_range[1]
    """
    inputpdf = create_reader(file)
    writer = create_writer()

    if len(split_range) > 2:
        raise ValueError("split_range should have only 2 integers")

    split_range.sort()
    low, high = split_range

    # total_pages = inputpdf.numPages
    for i in range(low, high):
        writer.addPage(inputpdf.getPage(i))

    return writer
