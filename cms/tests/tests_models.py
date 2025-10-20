"""
Tests for the Story model.

What we cover:
1) Basic creation: fields persist as expected; created_at is a datetime.
2) File/Image field semantics: how to correctly assert "no file".
3) __str__ returns the intended human-readable label.
4) Validation with a valid JPEG upload.
5) Validation failure for invalid extension (only if the model enforces it).

Why the extra care around File/Image fields?
- Django exposes FileField/ImageField values as a FieldFile object.
- When no file is set, that object is still present but evaluates to False.
- name is either "" (blank) OR None depending on `null=True` vs `null=False`.
  We assert in a way that works for both configurations.
"""

from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import models

from ..core.model_stories import Story

# Pillow is only required if story_photo is an ImageField, because ImageField
# actually attempts to identify/parse the image. If it's a plain FileField,
# Pillow isn't needed.
try:
    from PIL import Image  # type: ignore
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


def _make_tiny_jpeg() -> bytes:
    """
    Create a minimal in-memory JPEG (1x1 px). This is useful to validate an ImageField
    without touching the filesystem.

    Returns:
        Raw JPEG bytes.
    """
    buf = BytesIO()
    # A 1x1 black pixel is enough to be a valid JPEG for Pillow.
    Image.new("RGB", (1, 1)).save(buf, "JPEG")
    buf.seek(0)
    return buf.getvalue()


class StoryModelTest(TestCase):
    """
    Tests for Story model behavior. We keep assertions resilient to common model
    variations (e.g., `null=True` vs `null=False` on File/Image fields, USE_TZ on/off).
    """

    def setUp(self):
        # Shared base payload for a Story. We deliberately set story_photo=None
        # because many apps allow optional uploads.
        self.story_data = {
            "user_email": "testuser@example.com",
            "student_name": "John Doe",
            "varsity_name": "University XYZ",
            "story_photo": None,
        }

    # ---------- Helpers (kept small + readable) ----------

    @staticmethod
    def _has_file_extension_validator(field: models.Field) -> bool:
        """
        Return True if the field has a FileExtensionValidator among its validators.
        We use this to decide whether it's fair to expect .txt to fail validation.
        """
        return any(isinstance(v, FileExtensionValidator) for v in field.validators)

    # ---------- Tests ----------

    def test_story_creation(self):
        """
        A Story can be saved; scalar fields persist; created_at is a datetime;
        and an empty file field behaves as a falsy FieldFile.
        """
        story = Story.objects.create(**self.story_data)

        # Scalar field checks: these should round-trip exactly.
        self.assertEqual(story.user_email, self.story_data["user_email"])
        self.assertEqual(story.student_name, self.story_data["student_name"])
        self.assertEqual(story.varsity_name, self.story_data["varsity_name"])

        # File/Image fields:
        # - The attribute is a FieldFile object (always), even when "empty".
        # - It evaluates to False when no file is set.
        self.assertFalse(
            story.story_photo,
            msg="Empty FileField/ImageField should be falsy (no file assigned).",
        )

        # Depending on model config:
        # - null=True  -> story.story_photo.name is None
        # - null=False -> story.story_photo.name is ""
        self.assertIn(
            getattr(story.story_photo, "name", None),
            (None, ""),
            msg="Empty FileField/ImageField name should be None or empty string.",
        )

        # created_at should be a datetime; timezone-awareness depends on USE_TZ.
        self.assertIsInstance(story.created_at, datetime, msg="created_at must be datetime.")
        if getattr(settings, "USE_TZ", False):
            self.assertTrue(
                timezone.is_aware(story.created_at),
                msg="created_at should be timezone-aware when USE_TZ=True.",
            )
        else:
            self.assertTrue(
                timezone.is_naive(story.created_at),
                msg="created_at should be naive when USE_TZ=False.",
            )

    def test_str_method_returns_student_name(self):
        """
        __str__ typically returns a human-friendly label; for Story we expect student_name.
        Adjust this test if your model's __str__ returns something else.
        """
        story = Story.objects.create(**self.story_data)
        self.assertEqual(
            str(story),
            self.story_data["student_name"],
            msg="__str__ should return student_name for Story.",
        )

    def test_valid_image_format_is_accepted(self):
        """
        If story_photo is:
          - ImageField: ensure a real JPEG passes validation (requires Pillow).
          - FileField: ensure a .jpg file name passes (validators check extension).
        We call full_clean() to run validators without needing to save to the DB.
        """
        field = Story._meta.get_field("story_photo")

        if isinstance(field, models.ImageField):
            if not PIL_AVAILABLE:
                self.skipTest("Pillow not installed; skipping ImageField validation path.")

            jpeg_bytes = _make_tiny_jpeg()
            uploaded = SimpleUploadedFile(
                "ok.jpg",
                jpeg_bytes,
                content_type="image/jpeg",  # Helpful for request-like flows; not strictly required by Django.
            )
        else:
            # For FileField, content isn't decoded as an image — validators (if any) will
            # typically check the extension; bytes can be anything.
            uploaded = SimpleUploadedFile("ok.jpg", b"dummy", content_type="image/jpeg")

        story = Story(
            user_email="user@example.com",
            student_name="Jane Doe",
            varsity_name="University A",
            story_photo=uploaded,
        )

        # Should NOT raise ValidationError if the field accepts JPEGs (either ImageField or allowed extension).
        story.full_clean()

    def test_invalid_image_format_is_rejected_if_validator_present(self):
        """
        Only assert failure for invalid extension if the model actually enforces it via
        FileExtensionValidator. If not present, we skip to avoid false failures.

        Note:
        - ImageField alone does not reject a file purely because of extension; it tries to parse image bytes.
        - If your app wants to reject by extension, add FileExtensionValidator([...]).
        """
        field = Story._meta.get_field("story_photo")

        if not self._has_file_extension_validator(field):
            self.skipTest("No FileExtensionValidator on story_photo; test not applicable.")

        bad = SimpleUploadedFile(
            "oops.txt",  # .txt deliberately wrong based on typical validators
            b"just some text",
            content_type="text/plain",
        )

        story = Story(
            user_email="user@example.com",
            student_name="Jane Doe",
            varsity_name="University A",
            story_photo=bad,
        )

        # With an extension validator in place, full_clean() should raise.
        with self.assertRaises(ValidationError):
            story.full_clean()
