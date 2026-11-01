import io

from PIL import Image, UnidentifiedImageError

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_IMAGE_SIDE = 2048
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


class ImageValidationError(ValueError):
    pass


def validate_and_prepare_image(content: bytes) -> tuple[bytes, str, dict]:
    if not content:
        raise ImageValidationError("The uploaded image is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise ImageValidationError(
            "Image size exceeds the 10 MB upload limit."
        )

    try:
        with Image.open(io.BytesIO(content)) as image:
            image_format = (image.format or "").upper()

            if image_format not in ALLOWED_FORMATS:
                raise ImageValidationError(
                    "Unsupported image format. Use JPEG, PNG, or WEBP."
                )

            image.verify()

        with Image.open(io.BytesIO(content)) as image:
            width, height = image.size

            if width > MAX_IMAGE_SIDE or height > MAX_IMAGE_SIDE:
                scale = MAX_IMAGE_SIDE / max(width, height)
                new_size = (
                    max(1, int(width * scale)),
                    max(1, int(height * scale)),
                )
                image = image.resize(new_size, Image.Resampling.LANCZOS)

            if image_format == "JPEG":
                output_format = "JPEG"
                extension = "jpg"
                mime_type = "image/jpeg"
            elif image_format == "PNG":
                output_format = "PNG"
                extension = "png"
                mime_type = "image/png"
            else:
                output_format = "WEBP"
                extension = "webp"
                mime_type = "image/webp"

            if output_format == "JPEG" and image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            buffer = io.BytesIO()
            image.save(
                buffer,
                format=output_format,
                quality=88,
                optimize=True,
            )

            prepared = buffer.getvalue()

    except ImageValidationError:
        raise
    except (UnidentifiedImageError, OSError) as exc:
        raise ImageValidationError(
            "The file is not a valid or readable image."
        ) from exc

    metadata = {
        "filename": "",
        "media_type": mime_type,
        "width": width,
        "height": height,
        "size_bytes": len(prepared),
        "extension": extension,
    }

    return prepared, mime_type, metadata
