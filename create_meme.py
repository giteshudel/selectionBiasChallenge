"""
Create the final statistics meme.
Assembles four panels (Reality, Your Model, Selection Bias, Estimate) into
a professional-looking four-panel meme demonstrating selection bias.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


def create_statistics_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150,
    background_color: str = "white"
) -> None:
    """
    Create a four-panel statistics meme demonstrating selection bias.
    
    Assembles all four components into a 1×4 layout (four panels side by side):
    - Reality: Original image
    - Your Model: Stippled image
    - Selection Bias: Block letter mask
    - Estimate: Masked stippled image (biased estimate)
    
    Parameters
    ----------
    original_img : np.ndarray
        Original grayscale image as 2D array (height, width) with values in [0, 1]
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
    block_letter_img : np.ndarray
        Block letter mask as 2D array (height, width) with values in [0, 1]
    masked_stipple_img : np.ndarray
        Masked stippled image as 2D array (height, width) with values in [0, 1]
    output_path : str
        Path where the meme image should be saved (e.g., "my_statistics_meme.png")
    dpi : int
        Resolution (dots per inch) for the output image. Higher values (150-300)
        provide better quality for publication. Default 150.
    background_color : str
        Background color for the meme. Can be matplotlib color strings like
        "white", "lightgray", "pink", etc. Default "white".
    
    Returns
    -------
    None
        Saves the meme image to the specified output_path.
    """
    # Get image dimensions - ensure all images are the same size
    img_height, img_width = original_img.shape
    
    # Validate that all images have the same dimensions
    images = [
        ("original_img", original_img),
        ("stipple_img", stipple_img),
        ("block_letter_img", block_letter_img),
        ("masked_stipple_img", masked_stipple_img)
    ]
    
    for name, img in images:
        if img.shape != (img_height, img_width):
            raise ValueError(
                f"All images must have the same dimensions. "
                f"{name} has shape {img.shape}, expected ({img_height}, {img_width})"
            )
    
    # Create figure with 1 row, 4 columns
    # Use a larger figure size to accommodate four panels side by side
    fig_width = img_width * 4 / dpi  # Scale width for 4 panels
    fig_height = img_height / dpi + 1  # Add extra height for labels and spacing
    
    fig = plt.figure(figsize=(fig_width, fig_height), facecolor=background_color)
    gs = gridspec.GridSpec(2, 4, figure=fig, height_ratios=[0.92, 0.08], 
                          hspace=0.05, wspace=0.05)
    
    # Panel labels
    labels = ["Reality", "Your Model", "Selection Bias", "Estimate"]
    
    # Create the four image panels
    for i, (img, label) in enumerate(zip(
        [original_img, stipple_img, block_letter_img, masked_stipple_img],
        labels
    )):
        # Image panel (top row)
        ax_img = fig.add_subplot(gs[0, i])
        ax_img.imshow(img, cmap='gray', vmin=0, vmax=1, aspect='auto')
        ax_img.axis('off')
        # Add border around image panel to showcase spacing
        for spine in ax_img.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1.5)
        
        # Label panel (bottom row)
        ax_label = fig.add_subplot(gs[1, i])
        ax_label.text(0.5, 0.5, label, 
                     ha='center', va='center',
                     fontsize=14, fontweight='bold',
                     transform=ax_label.transAxes)
        ax_label.set_facecolor(background_color)
        ax_label.axis('off')
        # Add border around label panel to showcase spacing
        for spine in ax_label.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1.5)
    
    # Add a subtle border around the entire figure
    fig.patch.set_edgecolor('black')
    fig.patch.set_linewidth(2)
    
    # Save the figure
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                facecolor=background_color, edgecolor='black', 
                pad_inches=0.1)
    plt.close()
    
    print(f"Created statistics meme: {output_path}")
    print(f"Meme dimensions: {img_height}×{img_width} pixels per panel")
    print(f"Output resolution: {dpi} DPI")
    print(f"Background color: {background_color}")
    print(f"Total figure size: {fig_width:.1f}×{fig_height:.1f} inches")

