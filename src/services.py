"""Provide services to client."""
import os

import pytesseract
from pdf2image import convert_from_path
from .utils import get_files_from_dir
from .split import split_pdf
from .temp_dir import tempdir_name


def get_text(image_path: str) -> str:
    """Extract text from images using tesseract and save it to a file."""
    text = pytesseract.image_to_string(image_path)
    return text


def convert_to_image(pdf_path: str):
    """
    Convert pdf file to image.

    Only load pdf file where number of pages is less than 30.
    """
    # title = os.path.basename(pdf_path)
    images = convert_from_path(pdf_path)
    for i in range(len(images)):
        yield images[i], i

        # op_name = f"images/{title}-{i}.jpg"
        # images[i].save(op_name, "JPEG")
        # print("saved {} image.".format(op_name))
