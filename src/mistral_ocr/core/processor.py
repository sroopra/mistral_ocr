"""OCR processor using Mistral AI."""

import json
import os
from pathlib import Path
from typing import Any

from mistralai import Mistral

from ..utils import combine_ocr_pages_to_markdown, create_data_url, encode_pdf_to_base64


class OCRProcessor:
    """OCR processor leveraging Mistral AI capabilities."""

    def __init__(self, api_key: str | None = None):
        """Initialize OCR processor.

        Args:
            api_key: Mistral AI API key. If not provided, will look for MISTRAL_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key is required. Set MISTRAL_API_KEY or pass api_key parameter."
            )

        self.client = Mistral(api_key=self.api_key)

    def process_pdf(self, pdf_path: str | Path, include_images: bool = True) -> str:
        """Process a PDF document and extract text as markdown.

        Args:
            pdf_path: Path to the PDF file.
            include_images: Whether to include images as base64 in markdown.

        Returns:
            Extracted content as markdown string.

        Raises:
            FileNotFoundError: If PDF file doesn't exist.
            Exception: For OCR processing errors.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Encode PDF to base64
            base64_pdf = encode_pdf_to_base64(pdf_path)

            # Create data URL
            document_url = create_data_url(base64_pdf, "application/pdf")

            # Call the OCR API
            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": document_url},
                include_image_base64=include_images,
            )

            # Convert to markdown
            markdown_content = combine_ocr_pages_to_markdown(ocr_response)

            return markdown_content

        except Exception as e:
            raise Exception(f"Error processing PDF {pdf_path}: {e}") from e

    def process_image(self, image_path: str | Path) -> str:
        """Process an image and extract text using OCR.

        Args:
            image_path: Path to the image file.

        Returns:
            Extracted text from the image.

        Raises:
            FileNotFoundError: If image file doesn't exist.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # For now, redirect to PDF processing for consistency
        # TODO: Implement direct image processing if needed
        return f"Direct image processing not yet implemented for: {image_path}"

    def get_ocr_response_info(self, pdf_path: str | Path) -> dict[str, Any]:
        """Get raw OCR response information for debugging.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Dictionary containing OCR response details.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            base64_pdf = encode_pdf_to_base64(pdf_path)
            document_url = create_data_url(base64_pdf, "application/pdf")

            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": document_url},
                include_image_base64=True,
            )

            # Convert response to JSON for inspection
            response_dict: dict[str, Any] = json.loads(ocr_response.model_dump_json())

            return response_dict

        except Exception as e:
            raise Exception(
                f"Error getting OCR response info for {pdf_path}: {e}"
            ) from e
