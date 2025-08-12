"""Command-line interface for Mistral OCR."""

import argparse
import sys
from pathlib import Path
from typing import Optional

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
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )
    
    parser.add_argument(
        "--output", "-o",
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


def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if parsed_args.verbose:
        print(f"Mistral OCR v{__version__}", file=sys.stderr)
    
    if not parsed_args.pdf_file:
        parser.print_help()
        return 1
    
    pdf_path = Path(parsed_args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        return 1
    
    if not pdf_path.suffix.lower() == '.pdf':
        print(f"Error: Input file must be a PDF: {pdf_path}", file=sys.stderr)
        return 1
    
    try:
        # Initialize OCR processor
        if parsed_args.verbose:
            print("Initializing OCR processor...", file=sys.stderr)
        
        processor = OCRProcessor(api_key=parsed_args.api_key)
        
        # Process PDF
        if parsed_args.verbose:
            print(f"Processing PDF: {pdf_path}", file=sys.stderr)
        
        markdown_content = processor.process_pdf(
            pdf_path, 
            include_images=parsed_args.include_images
        )
        
        # Output results
        if parsed_args.output:
            output_path = Path(parsed_args.output)
            output_path.write_text(markdown_content, encoding='utf-8')
            if parsed_args.verbose:
                print(f"Markdown saved to: {output_path}", file=sys.stderr)
        else:
            print(markdown_content)
        
        if parsed_args.verbose:
            print("Processing completed successfully", file=sys.stderr)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if parsed_args.debug:
            import traceback
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())