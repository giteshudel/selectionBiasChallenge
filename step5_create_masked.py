"""
Step 5: Create a masked stippled image for the statistics meme.
Applies a block letter mask to the stippled image to demonstrate selection bias.
"""

import numpy as np


def create_masked_stipple(
    stipple_img: np.ndarray,
    mask_img: np.ndarray,
    threshold: float = 0.5
) -> np.ndarray:
    """
    Apply a block letter mask to the stippled image to create a biased estimate.
    
    Where the mask is dark (below threshold), stipples are removed (set to white/1.0).
    Where the mask is light (above threshold), stipples are kept as they are.
    
    This creates the "biased estimate" by systematically removing data points
    in the pattern of the mask, demonstrating selection bias.
    
    Parameters
    ----------
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
        Where 0.0 = black stipple dot, 1.0 = white background
    mask_img : np.ndarray
        Mask image as 2D array (height, width) with values in [0, 1]
        Where 0.0 = black (mask area - remove stipples), 1.0 = white (keep area)
    threshold : float
        Threshold value to determine what counts as part of the mask.
        Pixels with mask values below this threshold are considered part of the mask.
        Default 0.5.
    
    Returns
    -------
    masked_stipple : np.ndarray
        2D numpy array (height, width) with values in [0, 1]
        Same shape as input images
        Where mask is dark (below threshold): white (1.0) - stipples removed
        Where mask is light (above threshold): original stipple values kept
    """
    # Validate input shapes match
    if stipple_img.shape != mask_img.shape:
        raise ValueError(
            f"Input images must have the same shape. "
            f"stipple_img shape: {stipple_img.shape}, "
            f"mask_img shape: {mask_img.shape}"
        )
    
    # Create a copy of the stipple image
    masked_stipple = stipple_img.copy()
    
    # Identify mask regions: where mask is below threshold (dark/mask area)
    # In these regions, we want to remove stipples by setting to white (1.0)
    mask_regions = mask_img < threshold
    
    # Apply the mask: set masked regions to white (remove stipples)
    masked_stipple[mask_regions] = 1.0
    
    # Calculate statistics for information
    total_pixels = stipple_img.size
    mask_pixels = np.sum(mask_regions)
    mask_percentage = (mask_pixels / total_pixels) * 100
    
    # Count stipples removed
    original_stipples = np.sum(stipple_img == 0.0)
    remaining_stipples = np.sum(masked_stipple == 0.0)
    removed_stipples = original_stipples - remaining_stipples
    
    print(f"Applied mask to stippled image")
    print(f"Mask threshold: {threshold}")
    print(f"Mask area: {mask_pixels} pixels ({mask_percentage:.2f}% of image)")
    print(f"Original stipples: {original_stipples}")
    print(f"Remaining stipples after masking: {remaining_stipples}")
    print(f"Stipples removed (selection bias): {removed_stipples}")
    print(f"Masked stipple image shape: {masked_stipple.shape}")
    
    return masked_stipple

