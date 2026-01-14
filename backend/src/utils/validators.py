import re
from typing import Optional
from pathlib import Path
import mimetypes


def validate_filename(filename: str) -> bool:
    """
    Validate that the filename is safe and has a proper format.
    """
    if not filename or len(filename.strip()) == 0:
        return False

    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r'\.\.',  # Directory traversal
        r'[<>:"/\\|?*]',  # Invalid Windows characters
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, filename):
            return False

    return True


def validate_file_size(file_size: int, max_size: int = 50 * 1024 * 1024) -> bool:  # 50MB default
    """
    Validate that the file size is within the allowed limit.

    Args:
        file_size: Size of the file in bytes
        max_size: Maximum allowed size in bytes (default 50MB)

    Returns:
        True if file size is valid, False otherwise
    """
    return 0 <= file_size <= max_size


def validate_file_type(content_type: str) -> bool:
    """
    Validate that the file type is allowed (PDF or TXT).

    Args:
        content_type: MIME type of the file

    Returns:
        True if file type is allowed, False otherwise
    """
    allowed_types = {
        "application/pdf",
        "text/plain",
        "text/txt",
        "application/msword",  # .doc
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # .docx
    }
    return content_type in allowed_types


def validate_content_type(content_type: str) -> bool:
    """
    Validate that the content type is a valid MIME type.
    """
    if not content_type:
        return True  # Allow None/empty

    # Basic MIME type validation (format: type/subtype)
    mime_pattern = r'^[a-z][a-z0-9+.-]*\/[a-z0-9+.-]+$'
    return bool(re.match(mime_pattern, content_type))


def validate_checksum(checksum: str) -> bool:
    """
    Validate that the checksum is a valid hex string.
    """
    if not checksum:
        return True  # Allow None/empty

    # Basic hex validation
    return bool(re.match(r'^[a-fA-F0-9]+$', checksum))


def get_content_type_from_filename(filename: str) -> str:
    """
    Guess the content type from the filename extension.
    """
    content_type, _ = mimetypes.guess_type(filename)
    return content_type or "application/octet-stream"


def validate_knowledge_doc_fields(
    filename: str,
    file_size: int,
    content_type: Optional[str] = None,
    checksum: Optional[str] = None
) -> tuple[bool, list[str]]:
    """
    Validate all KnowledgeDoc fields and return (is_valid, errors).
    """
    errors = []

    if not validate_filename(filename):
        errors.append("Invalid filename format")

    if not validate_file_size(file_size):
        errors.append("File size must be non-negative")

    if content_type and not validate_content_type(content_type):
        errors.append("Invalid content type format")

    if checksum and not validate_checksum(checksum):
        errors.append("Invalid checksum format")

    return len(errors) == 0, errors