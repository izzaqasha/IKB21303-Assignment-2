import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# ============================================================
# FILE SIZE ANALYSIS
# ============================================================

def get_file_size(file_path):
    """Return the file size of a given file path in bytes."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return os.path.getsize(file_path)


def compare_file_sizes(cover_image_path, stego_image_path):
    """Compare the file sizes of the cover and stego images."""

    print("\n--- FILE SIZE COMPARISON ---\n")

    # Get file sizes
    cover_size = get_file_size(cover_image_path)
    stego_size = get_file_size(stego_image_path)

    # Calculate size difference
    difference = stego_size - cover_size

    # Calculate percentage difference
    if cover_size != 0:
        percentage = (difference / cover_size) * 100
    else:
        percentage = 0

    # Display results
    print(f"Cover image: {cover_image_path}")
    print(f"Cover image size: {cover_size} bytes")
    print()

    print(f"Stego image: {stego_image_path}")
    print(f"Stego image size: {stego_size} bytes")
    print()

    print(f"Size difference: {difference} bytes")
    print(f"Percentage difference: {percentage:.2f}%")

    return cover_size, stego_size, difference, percentage


# ============================================================
# HISTOGRAM ANALYSIS
# ============================================================

## Generate high-clarity RGB histograms (Classic Overlap / Silhouette Style)
def generate_histogram(cover_image_path, stego_image_path):
    """Generate high-clarity RGB histograms with clean visual overlap."""
    print("\n--- HISTOGRAM ANALYSIS ---\n")

    os.makedirs("output", exist_ok=True)

    # Load images using Pillow
    cover_image = Image.open(cover_image_path).convert("RGB")
    stego_image = Image.open(stego_image_path).convert("RGB")

    cover_channels = cover_image.split()
    stego_channels = stego_image.split()

    channel_names = ["Red", "Green", "Blue"]

    for i in range(3):
        plt.figure(figsize=(10, 5))

        # Cover Image (Blue)
        plt.hist(
            cover_channels[i].getdata(),
            bins=256,
            range=(0, 256),
            alpha=0.55,
            color="#1f77b4",
            label="Cover Image"
        )

        # Stego Image (Orange) - overlays on top creating the brown silhouette
        plt.hist(
            stego_channels[i].getdata(),
            bins=256,
            range=(0, 256),
            alpha=0.55,
            color="#ff7f0e",
            label="Stego Image"
        )

        # Formatting
        plt.title(f"{channel_names[i]} Channel Histogram (Color Distribution)", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Pixel Value (0 - 255)", fontsize=10, fontweight="bold")
        plt.ylabel("Frequency (Pixel Count)", fontsize=10, fontweight="bold")
        plt.xlim(0, 255)

        # Clean grid and legend
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.legend(
            loc="upper right",
            title="Overlap (Brown) = Identical Distribution",
            fontsize=10,
            title_fontsize=10,
            framealpha=0.9
        )

        plt.tight_layout()

        output_path = f"output/{channel_names[i].lower()}_histogram.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"{channel_names[i]} histogram saved to: {output_path}")

    print("\nHistogram analysis completed successfully.")

# ============================================================
# PIXEL DIFFERENCE ANALYSIS
# ============================================================

def analyze_pixel_differences(cover_image_path, stego_image_path):
    """Analyze pixel-level differences between two images."""

    print("\n--- PIXEL DIFFERENCE ANALYSIS ---\n")

    # Load both images
    cover_image = Image.open(cover_image_path).convert("RGB")
    stego_image = Image.open(stego_image_path).convert("RGB")

    # Ensure both images have the same dimensions
    if cover_image.size != stego_image.size:
        raise ValueError(
            "Cover and stego images must have the same dimensions."
        )

    # Convert image pixels into lists
    cover_pixels = list(cover_image.getdata())
    stego_pixels = list(stego_image.getdata())

    total_pixels = len(cover_pixels)

    # Initialize analysis variables
    changed_pixels = 0
    changed_channels = 0
    total_difference = 0
    maximum_difference = 0

    # Compare every pixel
    for cover_pixel, stego_pixel in zip(
        cover_pixels,
        stego_pixels
    ):

        pixel_changed = False

        # Compare Red, Green, and Blue values
        for cover_value, stego_value in zip(
            cover_pixel,
            stego_pixel
        ):

            difference = abs(
                cover_value - stego_value
            )

            if difference != 0:
                changed_channels += 1
                pixel_changed = True

            total_difference += difference

            if difference > maximum_difference:
                maximum_difference = difference

        # Count pixels that contain at least one changed channel
        if pixel_changed:
            changed_pixels += 1

    # Calculate percentage of changed pixels
    changed_pixel_percentage = (
        changed_pixels / total_pixels
    ) * 100

    # Display results
    print(f"Total pixels: {total_pixels}")
    print(f"Changed pixels: {changed_pixels}")

    print(
        f"Changed pixel percentage: "
        f"{changed_pixel_percentage:.2f}%"
    )

    print(f"Changed RGB channels: {changed_channels}")
    print(
        f"Total channel-value difference: "
        f"{total_difference}"
    )

    print(
        f"Maximum channel difference: "
        f"{maximum_difference}"
    )

    print(
        "\nPixel difference analysis completed successfully."
    )

    return (
        total_pixels,
        changed_pixels,
        changed_pixel_percentage,
        changed_channels,
        total_difference,
        maximum_difference
    )


# ============================================================
# STEGANALYSIS RESULT
# ============================================================

def generate_analysis_result(
    cover_image_path,
    stego_image_path,
    size_difference,
    size_percentage,
    changed_pixels,
    changed_pixel_percentage,
    changed_channels,
    total_difference,
    maximum_difference
):
    """Generate a summary of the steganalysis results."""

    print("\n--- STEGANALYSIS RESULT ---\n")

    print(f"Cover image: {cover_image_path}")
    print(f"Stego image: {stego_image_path}")
    print()

    # --------------------------------------------------------
    # File Size Analysis
    # --------------------------------------------------------

    print("### File Size Analysis ###")
    print(f"Size difference: {size_difference} bytes")
    print(
        f"Size difference percentage: "
        f"{size_percentage:.2f}%"
    )
    print()

    # --------------------------------------------------------
    # Pixel Difference Analysis
    # --------------------------------------------------------

    print("### Pixel Difference Analysis ###")
    print(f"Changed pixels: {changed_pixels}")

    print(
        f"Changed pixel percentage: "
        f"{changed_pixel_percentage:.2f}%"
    )

    print(f"Changed RGB channels: {changed_channels}")

    print(
        f"Total channel-value difference: "
        f"{total_difference}"
    )

    print(
        f"Maximum channel difference: "
        f"{maximum_difference}"
    )

    print()

    # --------------------------------------------------------
    # Basic Interpretation
    # --------------------------------------------------------

    if changed_pixels > 0:
        result = "MINOR PIXEL-LEVEL MODIFICATIONS DETECTED"
    else:
        result = "NO PIXEL-LEVEL MODIFICATIONS DETECTED"

    print("### Analysis Conclusion ###")
    print(f"Result: {result}")

    print(
        "\nNote: This result indicates pixel-level differences "
        "between the cover and stego images. It does not by "
        "itself prove that hidden data exists."
    )

    print(
        "\nSteganalysis result generated successfully."
    )

    return result


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # Define input and output image paths
    cover_image = "cover_images/cover.png"
    stego_image = "output/stego.png"

    # --------------------------------------------------------
    # 1. File Size Analysis
    # --------------------------------------------------------

    (
        cover_size,
        stego_size,
        size_difference,
        size_percentage
    ) = compare_file_sizes(
        cover_image,
        stego_image
    )

    # --------------------------------------------------------
    # 2. Histogram Analysis
    # --------------------------------------------------------

    generate_histogram(
        cover_image,
        stego_image
    )

    # --------------------------------------------------------
    # 3. Pixel Difference Analysis
    # --------------------------------------------------------

    (
        total_pixels,
        changed_pixels,
        changed_pixel_percentage,
        changed_channels,
        total_difference,
        maximum_difference
    ) = analyze_pixel_differences(
        cover_image,
        stego_image
    )

    # --------------------------------------------------------
    # 4. Generate Final Analysis Result
    # --------------------------------------------------------

    generate_analysis_result(
        cover_image,
        stego_image,
        size_difference,
        size_percentage,
        changed_pixels,
        changed_pixel_percentage,
        changed_channels,
        total_difference,
        maximum_difference
    )