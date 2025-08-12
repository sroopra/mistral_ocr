"""Command-line interface for Mistral OCR."""

import argparse
import logging
import sys
import traceback
from pathlib import Path

from . import __version__
from .core import OCRProcessor


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="mistral-ocr",
        description="Convert PDF documents to Markdown using Mistral AI OCR",
        epilog="""
Examples:
  mistral-ocr document.pdf                    # Output to stdout
  mistral-ocr document.pdf -o output.md       # Save to file
  mistral-ocr document.pdf --verbose          # Show progress
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (default: stdout)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="Mistral API key (default: MISTRAL_API_KEY env var)",
    )

    parser.add_argument(
        "--include-images",
        action="store_true",
        default=True,
        help="Include images as base64 in markdown (default: True)",
    )

    parser.add_argument(
        "pdf_file",
        nargs="?",
        help="Input PDF file for OCR processing",
    )

    return parser


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Setup logging
    log_level = (
        logging.DEBUG
        if parsed_args.debug
        else logging.INFO
        if parsed_args.verbose
        else logging.WARNING
    )
    logging.basicConfig(level=log_level, format="%(message)s")
    logger = logging.getLogger(__name__)

    if parsed_args.verbose:
        logger.info(f"Mistral OCR v{__version__}")

    if not parsed_args.pdf_file:
        parser.print_help()
        return 1

    pdf_path = Path(parsed_args.pdf_file)
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return 1

    if pdf_path.suffix.lower() != ".pdf":
        logger.error(f"Input file must be a PDF: {pdf_path}")
        return 1

    try:
        # Initialize OCR processor
        logger.info("Initializing OCR processor...")

        processor = OCRProcessor(api_key=parsed_args.api_key)

        # Process PDF
        logger.info(f"Processing PDF: {pdf_path}")

        markdown_content = processor.process_pdf(
            pdf_path, include_images=parsed_args.include_images
        )

        # Output results
        if parsed_args.output:
            output_path = Path(parsed_args.output)
            output_path.write_text(markdown_content, encoding="utf-8")
            logger.info(f"Markdown saved to: {output_path}")
        else:
            sys.stdout.write(markdown_content)

        logger.info("Processing completed successfully")

        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        if parsed_args.debug:
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
