from src.services import convert_to_image
from loguru import logger


def test_convert_to_image():
    input_file = "/home/igaurab/workspaces/pdf-ocr/test/test.pdf"
    for image in convert_to_image(input_file):
        assert image
