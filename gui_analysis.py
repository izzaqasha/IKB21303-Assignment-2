import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from analysis import (
    analyze_pixel_differences,
    compare_file_sizes,
    generate_analysis_result,
    generate_histogram,
)

# ==========================================================
# COLOR THEME & CONFIGURATION
# ==========================================================
BG_COLOR = "#F8FAFC"  # Light slate background
CARD_BG = "#FFFFFF"  # White card containers
TEXT_COLOR = "#0F172A"  # Deep slate text
MUTED_TEXT = "#64748B"  # Subdued gray text
BORDER_COLOR = "#CBD5E1"  # Subtle borders
PRIMARY_BTN = "#2563EB"  # Royal blue action button
PRIMARY_HOVER = "#1D4ED8"  # Darker blue on hover
SUCCESS_COLOR = "#16A34A"  # Green status
ERROR_COLOR = "#DC2626"  # Red status

root = tk.Tk()
root.title("Steganalysis Tool")
root.geometry("740x660")
root.minsize(740, 660)
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# Micro-interaction helper for hover states
def on_btn_enter(event):
    event.widget.config(bg=PRIMARY_HOVER)


def on_btn_leave(event):
    event.widget.config(bg=PRIMARY_BTN)


def show_image_preview(file_path, preview_label):
    image = Image.open(file_path)
    image.thumbnail((250, 150))
    photo = ImageTk.PhotoImage(image)
    preview_label.config(image=photo, text="", bg=CARD_BG)
    preview_label.image = photo


def select_analysis_cover():
    file_path = filedialog.askopenfilename(
        title="Select Cover Image",
        filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
    )
    if file_path:
        analysis_cover_entry.delete(0, tk.END)
        analysis_cover_entry.insert(0, file_path)
        show_image_preview(file_path, cover_preview_label)


def select_analysis_stego():
    file_path = filedialog.askopenfilename(
        title="Select Stego Image",
        filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")],
    )
    if file_path:
        analysis_stego_entry.delete(0, tk.END)
        analysis_stego_entry.insert(0, file_path)
        show_image_preview(file_path, stego_preview_label)


def run_steganalysis():
    cover_image = analysis_cover_entry.get()
    stego_image = analysis_stego_entry.get()
    status_label.config(text="Status: Running steganalysis...", fg="#0284C7")
    root.update_idletasks()

    if not cover_image or not stego_image:
        messagebox.showwarning(
            "Missing Information",
            "Please select both the cover image and stego image.",
        )
        return

    try:
        cover_size, stego_size, size_difference, size_percentage = (
            compare_file_sizes(cover_image, stego_image)
        )
        generate_histogram(cover_image, stego_image)
        (
            total_pixels,
            changed_pixels,
            changed_pixel_percentage,
            changed_channels,
            total_difference,
            maximum_difference,
        ) = analyze_pixel_differences(cover_image, stego_image)
        result = generate_analysis_result(
            cover_image,
            stego_image,
            size_difference,
            size_percentage,
            changed_pixels,
            changed_pixel_percentage,
            changed_channels,
            total_difference,
            maximum_difference,
        )

        status_label.config(
            text="Status: Analysis completed successfully!", fg=SUCCESS_COLOR
        )

        messagebox.showinfo(
            "Steganalysis Result",
            f"Analysis completed successfully!\n\n"
            f"---- FILE SIZE ANALYSIS ----\n\n"
            f"Cover image size: {cover_size:,} bytes\n"
            f"Stego image size: {stego_size:,} bytes\n"
            f"Size difference: {size_difference:+,} bytes\n"
            f"Percentage difference: {size_percentage:+.2f}%\n\n"
            f"---- PIXEL DIFFERENCE ANALYSIS ----\n\n"
            f"Changed pixels: {changed_pixels:,}\n"
            f"Changed pixel percentage: {changed_pixel_percentage:.2f}%\n"
            f"Changed RGB channels: {changed_channels:,}\n"
            f"Total channel-value difference: {total_difference:,}\n"
            f"Maximum channel difference: {maximum_difference}\n\n"
            f"---- CONCLUSION ----\n"
            f"{result}\n\n"
            f"RGB histograms were saved to the output folder.",
        )
    except Exception as error:
        status_label.config(text="Status: Error during analysis", fg=ERROR_COLOR)
        messagebox.showerror("Steganalysis Error", f"An error occurred:\n\n{error}")


# ==========================================================
# HEADER
# ==========================================================
title_label = tk.Label(
    root,
    text="Steganalysis Tool",
    font=("Segoe UI", 20, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
)
title_label.pack(pady=(20, 4))

info_label = tk.Label(
    root,
    text="Inspect, analyze pixel distributions, and evaluate steganographic artifacts",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=MUTED_TEXT,
)
info_label.pack(pady=(0, 15))


# ==========================================================
# STEGANALYSIS CARD FRAME
# ==========================================================
analysis_frame = tk.LabelFrame(
    root,
    text=" Image Steganalysis ",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    padx=20,
    pady=15,
)
analysis_frame.pack(padx=35, pady=5, fill="x")

content_frame = tk.Frame(analysis_frame, bg=CARD_BG)
content_frame.pack(anchor="center")

# --- Row 0: Cover Image ---
tk.Label(
    content_frame,
    text="Cover Image:",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR,
).grid(row=0, column=0, sticky="w", pady=6)

analysis_cover_entry = tk.Entry(
    content_frame, width=50, font=("Segoe UI", 9), relief="solid", bd=1
)
analysis_cover_entry.grid(row=0, column=1, padx=10)

tk.Button(
    content_frame,
    text="Browse...",
    font=("Segoe UI", 9),
    bg="#F1F5F9",
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    cursor="hand2",
    padx=8,
    pady=2,
    command=select_analysis_cover,
).grid(row=0, column=2)

# --- Row 1: Stego Image ---
tk.Label(
    content_frame,
    text="Stego Image:",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR,
).grid(row=1, column=0, sticky="w", pady=6)

analysis_stego_entry = tk.Entry(
    content_frame, width=50, font=("Segoe UI", 9), relief="solid", bd=1
)
analysis_stego_entry.grid(row=1, column=1, padx=10)

tk.Button(
    content_frame,
    text="Browse...",
    font=("Segoe UI", 9),
    bg="#F1F5F9",
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    cursor="hand2",
    padx=8,
    pady=2,
    command=select_analysis_stego,
).grid(row=1, column=2)

# --- Previews Row ---
preview_frame = tk.Frame(content_frame, bg=CARD_BG)
preview_frame.grid(row=2, column=0, columnspan=3, pady=16)

# Cover Image Preview Box
cover_container = tk.Frame(
    preview_frame, width=250, height=150, bg="#F8FAFC", relief="solid", bd=1
)
cover_container.grid(row=0, column=0, padx=14)
cover_container.pack_propagate(False)

cover_preview_label = tk.Label(
    cover_container,
    text="No Cover Selected\n(Browse cover image above)",
    font=("Segoe UI", 9, "italic"),
    fg=MUTED_TEXT,
    bg="#F8FAFC",
    justify="center",
)
cover_preview_label.pack(expand=True, fill="both")

# Stego Image Preview Box
stego_container = tk.Frame(
    preview_frame, width=250, height=150, bg="#F8FAFC", relief="solid", bd=1
)
stego_container.grid(row=0, column=1, padx=14)
stego_container.pack_propagate(False)

stego_preview_label = tk.Label(
    stego_container,
    text="No Stego Selected\n(Browse stego image above)",
    font=("Segoe UI", 9, "italic"),
    fg=MUTED_TEXT,
    bg="#F8FAFC",
    justify="center",
)
stego_preview_label.pack(expand=True, fill="both")

# --- Action: Run Steganalysis ---
analysis_button = tk.Button(
    content_frame,
    text="RUN STEGANALYSIS",
    font=("Segoe UI", 10, "bold"),
    bg=PRIMARY_BTN,
    fg="#FFFFFF",
    activebackground=PRIMARY_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    width=24,
    pady=6,
    command=run_steganalysis,
)
analysis_button.grid(row=3, column=0, columnspan=3, pady=(10, 5))
analysis_button.bind("<Enter>", on_btn_enter)
analysis_button.bind("<Leave>", on_btn_leave)

# ==========================================================
# STATUS BAR & FOOTER
# ==========================================================
status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=MUTED_TEXT,
    anchor="w",
)
status_label.pack(side="bottom", fill="x", padx=35, pady=10)

root.mainloop()
