"""Mistral OCR - OCR project leveraging Mistral AI capabilities."""

import sys

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import OCRProcessor

__all__ = ["OCRProcessor"]


def main() -> None:
    """Main entry point placeholder."""
    from .__main__ import main as cli_main

    sys.exit(cli_main())
