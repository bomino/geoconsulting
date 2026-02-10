import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.core.validators import (
    MAX_FILE_SIZE,
    validate_document_file,
    validate_image_file,
)


class TestImageValidator:
    @pytest.mark.parametrize("ext", [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"])
    def test_valid_extensions(self, ext):
        f = SimpleUploadedFile(f"test{ext}", b"data", content_type="application/octet-stream")
        validate_image_file(f)

    def test_invalid_extension_raises(self):
        f = SimpleUploadedFile("test.exe", b"data", content_type="application/octet-stream")
        with pytest.raises(ValidationError):
            validate_image_file(f)


class TestDocumentValidator:
    @pytest.mark.parametrize("ext", [".pdf", ".docx", ".xlsx", ".png", ".jpg", ".jpeg", ".gif"])
    def test_valid_extensions(self, ext):
        f = SimpleUploadedFile(f"test{ext}", b"data", content_type="application/octet-stream")
        validate_document_file(f)

    def test_invalid_extension_raises(self):
        f = SimpleUploadedFile("test.py", b"data", content_type="application/octet-stream")
        with pytest.raises(ValidationError):
            validate_document_file(f)


class TestFileSizeLimit:
    def test_file_over_limit_raises(self):
        f = SimpleUploadedFile("big.png", b"x", content_type="application/octet-stream")
        f.size = MAX_FILE_SIZE + 1
        with pytest.raises(ValidationError):
            validate_image_file(f)

    def test_file_at_limit_passes(self):
        f = SimpleUploadedFile("ok.png", b"x", content_type="application/octet-stream")
        f.size = MAX_FILE_SIZE
        validate_image_file(f)
