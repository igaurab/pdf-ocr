"""Factory functions for reading and writing pdf files."""

from PyPDF2 import PdfFileReader, PdfFileWriter
from .test_pypdf import TestReader, TestWriter


def create_reader(file, test=False):
    """Create instance of reader."""
    if test:
        return TestReader()
    return PdfFileReader(file, "rb")


def create_writer(test=False):
    """Create instance of writer."""
    if test:
        return TestWriter()
    return PdfFileWriter()
