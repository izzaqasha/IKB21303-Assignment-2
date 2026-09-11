import tkinter as tk
from tkinter import filedialog, messagebox

from steganography import hide_file, extract_file
from integrity import calculate_sha256

from analysis import (
    compare_file_sizes,
    generate_histogram,
    analyze_pixel_differences,
    generate_analysis_result
)


# Create the main application window
root = tk.Tk()

root.title("Steganography Tool")
root.geometry("800x1150")
root.resizable(False, False)


# ==========================================================
# TITLE
# ==========================================================

title_label = tk.Label(
    root,
    text="STEGANOGRAPHY TOOL",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=25)


info_label = tk.Label(
    root,
    text="Hide, extract, and analyze hidden files",
    font=("Arial", 12)
)

info_label.pack(pady=5)


# ==========================================================
# HIDE FILE SECTION
# ==========================================================

hide_frame = tk.LabelFrame(
    root,
    text="Hide File",
    font=("Arial", 13, "bold"),
    padx=15,
    pady=15
)

hide_frame.pack(
    padx=40,
    pady=25,
    fill="x"
)


# Cover image
cover_label = tk.Label(
    hide_frame,
    text="Cover Image:"
)

cover_label.grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)


cover_entry = tk.Entry(
    hide_frame,
    width=60
)

cover_entry.grid(
    row=0,
    column=1,
    padx=10
)


def select_cover_image():
    file_path = filedialog.askopenfilename(
        title="Select Cover Image",
        filetypes=[
            ("PNG Images", "*.png"),
            ("JPEG Images", "*.jpg"),
            ("JPEG Images", "*.jpeg"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        cover_entry.delete(0, tk.END)
        cover_entry.insert(0, file_path)


cover_button = tk.Button(
    hide_frame,
    text="Browse...",
    command=select_cover_image
)

cover_button.grid(
    row=0,
    column=2
)


# Secret file
secret_label = tk.Label(
    hide_frame,
    text="Secret File:"
)

secret_label.grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)


secret_entry = tk.Entry(
    hide_frame,
    width=60
)

secret_entry.grid(
    row=1,
    column=1,
    padx=10
)


def select_secret_file():
    file_path = filedialog.askopenfilename(
        title="Select Secret File",
        filetypes=[
            ("All Files", "*.*")
        ]
    )

    if file_path:
        secret_entry.delete(0, tk.END)
        secret_entry.insert(0, file_path)


secret_button = tk.Button(
    hide_frame,
    text="Browse...",
    command=select_secret_file
)

secret_button.grid(
    row=1,
    column=2
)


# Output image
output_label = tk.Label(
    hide_frame,
    text="Output Image:"
)

output_label.grid(
    row=2,
    column=0,
    sticky="w",
    pady=8
)


output_entry = tk.Entry(
    hide_frame,
    width=60
)

output_entry.grid(
    row=2,
    column=1,
    padx=10
)


def select_output_image():
    file_path = filedialog.asksaveasfilename(
        title="Save Stego Image",
        defaultextension=".png",
        filetypes=[
            ("PNG Images", "*.png")
        ]
    )

    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)


output_button = tk.Button(
    hide_frame,
    text="Browse...",
    command=select_output_image
)

output_button.grid(
    row=2,
    column=2
)


# ==========================================================
# HIDE FILE FUNCTION
# ==========================================================

def run_hide_file():

    cover_image = cover_entry.get()
    secret_file = secret_entry.get()
    output_image = output_entry.get()

    # Check that all fields are filled
    if not cover_image or not secret_file or not output_image:
        messagebox.showwarning(
            "Missing Information",
            "Please select the cover image, secret file, and output image."
        )
        return

    try:

        hide_file(
            cover_image,
            secret_file,
            output_image
        )

        messagebox.showinfo(
            "Success",
            "Secret file hidden successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"An error occurred:\n\n{error}"
        )


# Hide button
hide_button = tk.Button(
    hide_frame,
    text="HIDE FILE",
    font=("Arial", 11, "bold"),
    width=20,
    command=run_hide_file
)

hide_button.grid(
    row=3,
    column=1,
    pady=15
)

# ==========================================================
# EXTRACT FILE SECTION
# ==========================================================

extract_frame = tk.LabelFrame(
    root,
    text="Extract File",
    font=("Arial", 13, "bold"),
    padx=15,
    pady=15
)

extract_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


# Stego image
stego_label = tk.Label(
    extract_frame,
    text="Stego Image:"
)

stego_label.grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)


stego_entry = tk.Entry(
    extract_frame,
    width=60
)

stego_entry.grid(
    row=0,
    column=1,
    padx=10
)


def select_stego_image():
    file_path = filedialog.askopenfilename(
        title="Select Stego Image",
        filetypes=[
            ("PNG Images", "*.png"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        stego_entry.delete(0, tk.END)
        stego_entry.insert(0, file_path)


stego_button = tk.Button(
    extract_frame,
    text="Browse...",
    command=select_stego_image
)

stego_button.grid(
    row=0,
    column=2
)


# Output directory
extract_output_label = tk.Label(
    extract_frame,
    text="Output Folder:"
)

extract_output_label.grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)


extract_output_entry = tk.Entry(
    extract_frame,
    width=60
)

extract_output_entry.grid(
    row=1,
    column=1,
    padx=10
)


def select_extract_output():
    folder_path = filedialog.askdirectory(
        title="Select Output Folder"
    )

    if folder_path:
        extract_output_entry.delete(0, tk.END)
        extract_output_entry.insert(0, folder_path)


extract_output_button = tk.Button(
    extract_frame,
    text="Browse...",
    command=select_extract_output
)

extract_output_button.grid(
    row=1,
    column=2
)


# ==========================================================
# EXTRACT FILE FUNCTION
# ==========================================================

def run_extract_file():

    stego_image = stego_entry.get()
    output_directory = extract_output_entry.get()

    # Check that all fields are filled
    if not stego_image or not output_directory:
        messagebox.showwarning(
            "Missing Information",
            "Please select the stego image and output folder."
        )
        return

    try:

        extract_file(
            stego_image,
            output_directory
        )

        messagebox.showinfo(
            "Success",
            "Secret file extracted successfully!"
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"An error occurred:\n\n{error}"
        )


# Extract button
extract_button = tk.Button(
    extract_frame,
    text="EXTRACT FILE",
    font=("Arial", 11, "bold"),
    width=20,
    command=run_extract_file
)

extract_button.grid(
    row=2,
    column=1,
    pady=15
)

# ==========================================================
# SHA-256 INTEGRITY VERIFICATION SECTION
# ==========================================================

integrity_frame = tk.LabelFrame(
    root,
    text="SHA-256 Integrity Verification",
    font=("Arial", 13, "bold"),
    padx=15,
    pady=15
)

integrity_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


# Original file
original_label = tk.Label(
    integrity_frame,
    text="Original File:"
)

original_label.grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)


original_entry = tk.Entry(
    integrity_frame,
    width=60
)

original_entry.grid(
    row=0,
    column=1,
    padx=10
)


def select_original_file():

    file_path = filedialog.askopenfilename(
        title="Select Original File",
        filetypes=[
            ("All Files", "*.*")
        ]
    )

    if file_path:
        original_entry.delete(0, tk.END)
        original_entry.insert(0, file_path)


original_button = tk.Button(
    integrity_frame,
    text="Browse...",
    command=select_original_file
)

original_button.grid(
    row=0,
    column=2
)


# Extracted file
extracted_label = tk.Label(
    integrity_frame,
    text="Extracted File:"
)

extracted_label.grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)


extracted_entry = tk.Entry(
    integrity_frame,
    width=60
)

extracted_entry.grid(
    row=1,
    column=1,
    padx=10
)


def select_extracted_file():

    file_path = filedialog.askopenfilename(
        title="Select Extracted File",
        filetypes=[
            ("All Files", "*.*")
        ]
    )

    if file_path:
        extracted_entry.delete(0, tk.END)
        extracted_entry.insert(0, file_path)


extracted_button = tk.Button(
    integrity_frame,
    text="Browse...",
    command=select_extracted_file
)

extracted_button.grid(
    row=1,
    column=2
)


# ==========================================================
# SHA-256 VERIFICATION FUNCTION
# ==========================================================

def run_integrity_check():

    original_file = original_entry.get()
    extracted_file = extracted_entry.get()

    # Check that both fields are filled
    if not original_file or not extracted_file:

        messagebox.showwarning(
            "Missing Information",
            "Please select both the original and extracted files."
        )

        return

    try:

        original_hash = calculate_sha256(original_file)
        extracted_hash = calculate_sha256(extracted_file)

        if original_hash == extracted_hash:

            messagebox.showinfo(
                "Integrity Verification",
                "SHA-256 hashes MATCH.\n\n"
                "Integrity verification: PASSED."
            )

        else:

            messagebox.showerror(
                "Integrity Verification",
                "SHA-256 hashes DO NOT MATCH.\n\n"
                "Integrity verification: FAILED."
            )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"An error occurred:\n\n{error}"
        )


# Verify button
integrity_button = tk.Button(
    integrity_frame,
    text="VERIFY INTEGRITY",
    font=("Arial", 11, "bold"),
    width=20,
    command=run_integrity_check
)

integrity_button.grid(
    row=2,
    column=1,
    pady=15
)

# ==========================================================
# STEGANALYSIS SECTION
# ==========================================================

analysis_frame = tk.LabelFrame(
    root,
    text="Steganalysis",
    font=("Arial", 13, "bold"),
    padx=15,
    pady=15
)

analysis_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


# Cover image
analysis_cover_label = tk.Label(
    analysis_frame,
    text="Cover Image:"
)

analysis_cover_label.grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)


analysis_cover_entry = tk.Entry(
    analysis_frame,
    width=60
)

analysis_cover_entry.grid(
    row=0,
    column=1,
    padx=10
)


def select_analysis_cover():

    file_path = filedialog.askopenfilename(
        title="Select Cover Image",
        filetypes=[
            ("PNG Images", "*.png"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        analysis_cover_entry.delete(0, tk.END)
        analysis_cover_entry.insert(0, file_path)


analysis_cover_button = tk.Button(
    analysis_frame,
    text="Browse...",
    command=select_analysis_cover
)

analysis_cover_button.grid(
    row=0,
    column=2
)


# Stego image
analysis_stego_label = tk.Label(
    analysis_frame,
    text="Stego Image:"
)

analysis_stego_label.grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)


analysis_stego_entry = tk.Entry(
    analysis_frame,
    width=60
)

analysis_stego_entry.grid(
    row=1,
    column=1,
    padx=10
)


def select_analysis_stego():

    file_path = filedialog.askopenfilename(
        title="Select Stego Image",
        filetypes=[
            ("PNG Images", "*.png"),
            ("All Files", "*.*")
        ]
    )

    if file_path:
        analysis_stego_entry.delete(0, tk.END)
        analysis_stego_entry.insert(0, file_path)


analysis_stego_button = tk.Button(
    analysis_frame,
    text="Browse...",
    command=select_analysis_stego
)

analysis_stego_button.grid(
    row=1,
    column=2
)


# ==========================================================
# RUN STEGANALYSIS
# ==========================================================

def run_steganalysis():

    cover_image = analysis_cover_entry.get()
    stego_image = analysis_stego_entry.get()

    # Check that both files are selected
    if not cover_image or not stego_image:

        messagebox.showwarning(
            "Missing Information",
            "Please select both the cover image and stego image."
        )

        return

    try:

        # --------------------------------------------------
        # File-size analysis
        # --------------------------------------------------

        (
            cover_size,
            stego_size,
            size_difference,
            size_percentage
        ) = compare_file_sizes(
            cover_image,
            stego_image
        )


        # --------------------------------------------------
        # Histogram analysis
        # --------------------------------------------------

        generate_histogram(
            cover_image,
            stego_image
        )


        # --------------------------------------------------
        # Pixel difference analysis
        # --------------------------------------------------

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


        # --------------------------------------------------
        # Generate final result
        # --------------------------------------------------

        result = generate_analysis_result(
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


        # --------------------------------------------------
        # Display result
        # --------------------------------------------------

        messagebox.showinfo(
            "Steganalysis Result",
            f"Analysis completed successfully!\n\n"
            f"Result:\n{result}\n\n"
            f"Changed pixels: {changed_pixels}\n"
            f"Changed pixel percentage: "
            f"{changed_pixel_percentage:.2f}%\n\n"
            f"Histograms were saved to the output folder."
        )

    except Exception as error:

        messagebox.showerror(
            "Steganalysis Error",
            f"An error occurred:\n\n{error}"
        )


# Run analysis button
analysis_button = tk.Button(
    analysis_frame,
    text="RUN STEGANALYSIS",
    font=("Arial", 11, "bold"),
    width=20,
    command=run_steganalysis
)

analysis_button.grid(
    row=2,
    column=1,
    pady=15
)

# ==========================================================
# START GUI
# ==========================================================

# Start the GUI
root.mainloop()

