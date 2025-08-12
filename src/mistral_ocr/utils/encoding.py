"""PDF encoding utilities."""

import base64
from pathlib import Path


def encode_pdf_to_base64(pdf_path: str | Path) -> str:
    """Encode a PDF file to base64 string.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Base64 encoded string of the PDF file.

    Raises:
        FileNotFoundError: If the PDF file doesn't exist.
        Exception: For other encoding errors.
    """
    pdf_path = Path(pdf_path)

    try:
        with pdf_path.open("rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The PDF file {pdf_path} was not found.") from e
    except Exception as e:
        raise Exception(f"Error encoding PDF file: {e}") from e


def create_data_url(base64_data: str, mime_type: str = "application/pdf") -> str:
    """Create a data URL from base64 encoded data.

    Args:
        base64_data: Base64 encoded data.
        mime_type: MIME type of the data.

    Returns:
        Data URL string.
    """
    return f"data:{mime_type};base64,{base64_data}"
