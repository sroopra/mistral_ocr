"""Markdown processing utilities."""

from typing import Dict
from mistralai.models import OCRResponse


def replace_images_in_markdown(markdown_str: str, images_dict: Dict[str, str]) -> str:
    """Replace image placeholders in markdown with base64-encoded images.

    Args:
        markdown_str: Markdown text containing image placeholders.
        images_dict: Dictionary mapping image IDs to base64 strings.

    Returns:
        Markdown text with images replaced by base64 data URLs.
    """
    for img_name, base64_str in images_dict.items():
        # Create data URL for the image
        data_url = f"data:image/jpeg;base64,{base64_str}"
        # Replace markdown image references
        markdown_str = markdown_str.replace(
            f"![{img_name}]({img_name})", f"![{img_name}]({data_url})"
        )
    return markdown_str


def combine_ocr_pages_to_markdown(ocr_response: OCRResponse) -> str:
    """Combine OCR pages into a single markdown document.

    Args:
        ocr_response: Response from OCR processing containing text and images.

    Returns:
        Combined markdown string with embedded images.
    """
    markdowns = []
    
    for page in ocr_response.pages:
        # Extract images from page
        image_data = {}
        for img in page.images:
            image_data[img.id] = img.image_base64
        
        # Replace image placeholders with actual base64 data
        page_markdown = replace_images_in_markdown(page.markdown, image_data)
        markdowns.append(page_markdown)
    
    # Join all pages with double newlines
    return "\n\n".join(markdowns)