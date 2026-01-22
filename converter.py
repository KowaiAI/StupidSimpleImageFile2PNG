"""Image conversion and metadata stripping logic."""

from pathlib import Path
from typing import Callable, Optional
from PIL import Image


SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif', '.png'}


def strip_metadata(image: Image.Image) -> Image.Image:
    """Remove all metadata from a PIL Image.

    Creates a new image with only pixel data, stripping EXIF, XMP, IPTC, etc.
    """
    data = list(image.getdata())

    if image.mode == 'RGBA':
        new_image = Image.new('RGBA', image.size)
    elif image.mode == 'LA':
        new_image = Image.new('LA', image.size)
    elif image.mode == 'P':
        # Convert palette images to RGBA to preserve transparency
        image = image.convert('RGBA')
        data = list(image.getdata())
        new_image = Image.new('RGBA', image.size)
    else:
        # Convert to RGB for formats without alpha
        image = image.convert('RGB')
        data = list(image.getdata())
        new_image = Image.new('RGB', image.size)

    new_image.putdata(data)
    return new_image


def convert_to_png(input_path: Path, output_folder: Path) -> Path:
    """Convert a single image to PNG format with metadata stripped.

    Args:
        input_path: Path to the source image
        output_folder: Directory where the PNG will be saved

    Returns:
        Path to the converted PNG file

    Raises:
        ValueError: If the file format is not supported
        IOError: If the file cannot be read or written
    """
    input_path = Path(input_path)
    output_folder = Path(output_folder)

    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {suffix}")

    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Generate output filename
    output_path = output_folder / f"{input_path.stem}.png"

    # Handle filename conflicts
    counter = 1
    while output_path.exists():
        output_path = output_folder / f"{input_path.stem}_{counter}.png"
        counter += 1

    # Open, strip metadata, and save
    with Image.open(input_path) as img:
        clean_image = strip_metadata(img)
        clean_image.save(output_path, 'PNG', optimize=True)

    return output_path


def batch_convert(
    file_list: list[Path],
    output_folder: Path,
    progress_callback: Optional[Callable[[int, int, str], None]] = None
) -> tuple[list[Path], list[tuple[Path, str]]]:
    """Convert multiple images to PNG format.

    Args:
        file_list: List of paths to source images
        output_folder: Directory where PNGs will be saved
        progress_callback: Optional callback(current, total, filename) for progress updates

    Returns:
        Tuple of (successful_paths, failed_items) where failed_items is list of (path, error_message)
    """
    successful = []
    failed = []
    total = len(file_list)

    for i, input_path in enumerate(file_list):
        input_path = Path(input_path)

        if progress_callback:
            progress_callback(i, total, input_path.name)

        try:
            output_path = convert_to_png(input_path, output_folder)
            successful.append(output_path)
        except Exception as e:
            failed.append((input_path, str(e)))

    # Final progress update
    if progress_callback:
        progress_callback(total, total, "Complete")

    return successful, failed
