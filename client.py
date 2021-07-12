"""Client code for terminal application."""

import os
import click

from loguru import logger

from src.services import get_text, convert_to_image
from src.split import split_pdf_range, split_pdf_batch
from src.temp_dir import tempdir_name
from src.utils import get_files_from_dir, get_filename, basedir_exists


def get_split_value(value: str):
    """Convert string to int and return appropriate result."""
    value = value.replace("=", "")
    split_range = value.split(",")
    split_range = [int(i) for i in split_range]
    return split_range


def split_pdf(file_path, split_range, output_path):
    """
    Split single pdf into multiple pdf's
    Saves the splitted pdf in output_path

    """
    filename = get_filename(file_path)

    if isinstance(split_range, list):
        low, high = split_range
        op_name = f"{output_path}/{filename}_{low}_{high}.pdf"
        output = split_pdf_range(file_path, split_range)
        with open(op_name, "wb") as pdf:
            output.write(pdf)
        logger.info(f"Split_pdf range: {op_name}")
    else:
        for low, high, output in split_pdf_batch(file_path, split_range):
            op_name = f"{output_path}/{filename}_{low}_{high}.pdf"
            with open(op_name, "wb") as pdf:
                output.write(pdf)
            logger.info(f"Split_pdf batch: {op_name}")


def perform_ocr(file: str, split_range, output_path):
    """Driver function."""
    # Create temporary dirs
    temp_pdf_dir = f"{tempdir_name}/pdf"
    temp_image_dir = f"{tempdir_name}/images"
    os.makedirs(temp_pdf_dir, exist_ok=True)
    os.makedirs(temp_image_dir, exist_ok=True)

    file = os.path.abspath(file)
    filename = get_filename(file)

    # Split pdf and save files in specified dir
    split_pdf(file_path=file, split_range=split_range, output_path=temp_pdf_dir)

    _files = get_files_from_dir(temp_pdf_dir)

    for file in _files:
        logger.info(f"Converting {file} to image")
        for image, index in convert_to_image(file):
            op_file = f"{temp_image_dir}/{filename}_{index}.jpg"
            image.save(op_file, "JPEG")
            logger.info(f"Saving image: {op_file}")

    # Perform OCR
    os.makedirs("text", exist_ok=True)
    _images = get_files_from_dir(temp_image_dir)
    # text = []
    for img in _images:
        title = os.path.basename(img)
        logger.info(f"OCR on image: {title}")
        txt = get_text(img)
        # text.append(txt)

        # file_content = " ".join(text)

        with open(f"text/{title}.txt", "w") as f:
            print(f"Writing to file: text/{title}.txt")
            f.write(txt)


@click.command("split")
@click.option("-f", help="Input file.")
@click.option("-s", help="Split pdf page by range or uniformly.")
@click.option("-o", help="Output folder.")
def cli(f, s, o):
    split_range = get_split_value(s)
    print(split_range)
    f = f.replace("=", "")
    f = os.path.abspath(f)
    perform_ocr(f, split_range, o)


if __name__ == "__main__":
    cli()
