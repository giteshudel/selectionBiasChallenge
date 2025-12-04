"""
Step 4: Create a block letter for the statistics meme.
Generates a block letter (default "S") matching the image dimensions.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import platform


def create_block_letter_s(
    height: int,
    width: int,
    letter: str = "S",
    font_size_ratio: float = 0.95,
    stroke_width: int = 0
) -> np.ndarray:
    """
    Create a block letter matching the specified image dimensions.
    
    Parameters
    ----------
    height : int
        Height of the output image in pixels
    width : int
        Width of the output image in pixels
    letter : str
        Letter to render (default "S"). Only single character is recommended.
    font_size_ratio : float
        Ratio of font size relative to the smaller dimension (0.0 to 1.0).
        Default 0.9 means the letter will be 90% of the smaller dimension.
    stroke_width : int
        Width of the stroke/outline to add to the letter in pixels.
        Default 0 means no additional stroke (just the font's natural thickness).
        Higher values create thicker/bolder letters.
    
    Returns
    -------
    block_letter : np.ndarray
        2D numpy array (height, width) with values in [0, 1]
        Black letter (0.0) on white background (1.0)
    """
    # Create a white image
    img = Image.new('L', (width, height), 255)  # 'L' mode = grayscale, 255 = white
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on the smaller dimension
    min_dimension = min(height, width)
    font_size = int(min_dimension * font_size_ratio * 1.15)  # Increased by 15%
    
    # Try to load a bold font
    # Different font paths for different operating systems
    font = None
    system = platform.system()
    
    font_paths = []
    if system == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
        ]
    elif system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
            "C:/Windows/Fonts/impact.ttf",
        ]
    else:  # Linux
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ]
    
    # Try to load a font from the system paths
    for font_path in font_paths:
        try:
            # For .ttc files (TrueType Collection), we need to specify the font index
            if font_path.endswith('.ttc'):
                font = ImageFont.truetype(font_path, font_size, index=0)
            else:
                font = ImageFont.truetype(font_path, font_size)
            print(f"Loaded font from: {font_path}")
            break
        except (OSError, IOError):
            continue
    
    # If no font found, use default font
    if font is None:
        try:
            # Try using the default truetype font
            font = ImageFont.truetype(font="arial.ttf", size=font_size)
        except (OSError, IOError):
            # Fall back to default bitmap font
            font = ImageFont.load_default()
            print("Using default bitmap font (may appear pixelated)")
    
    # Get text bounding box to center the letter
    if font:
        # Use textbox for better positioning
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        text_width = width // 2
        text_height = height // 2
 
    
    # Calculate centered position
    x = (width - text_width) // 2 - (bbox[0] if font else 0)
    y = (height - text_height) // 2 - (bbox[1] if font else 0)
    
    # Draw the letter in black (0 = black in grayscale mode)
    # Add stroke width if specified
    if stroke_width > 0:
        try:
            # Try using stroke_width parameter (Pillow 8.0+)
            draw.text((x, y), letter, fill=0, font=font, 
                     stroke_width=stroke_width, stroke_fill=0)
        except TypeError:
            # Fallback for older PIL versions: draw multiple offset copies
            # Draw outline by drawing letter at multiple offsets
            for dx in range(-stroke_width, stroke_width + 1):
                for dy in range(-stroke_width, stroke_width + 1):
                    if dx*dx + dy*dy <= stroke_width*stroke_width:  # Circular pattern
                        draw.text((x + dx, y + dy), letter, fill=0, font=font)
            # Draw main letter on top
            draw.text((x, y), letter, fill=0, font=font)
    else:
        # No stroke, just draw the letter normally
        draw.text((x, y), letter, fill=0, font=font)
    
    # Convert PIL image to numpy array and normalize to [0, 1]
    # PIL uses 0-255, we want 0-1 where 0 = black, 1 = white
    img_array = np.array(img, dtype=np.float32) / 255.0
    
    # Invert so that black is 0.0 and white is 1.0
    # Actually, PIL 'L' mode: 0 = black, 255 = white
    # After normalization: 0.0 = black, 1.0 = white
    # This matches the requirement: black letter (0.0) on white background (1.0)
    
    print(f"Created block letter '{letter}' with size {font_size}px")
    if stroke_width > 0:
        print(f"Stroke width: {stroke_width} pixels")
    print(f"Block letter image shape: {img_array.shape}")
    print(f"Letter dimensions: {text_width}x{text_height} pixels")
    
    return img_array

