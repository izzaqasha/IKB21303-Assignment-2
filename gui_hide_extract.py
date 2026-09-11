import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Import the core steganography functions from another module
from steganography import hide_file, extract_file

# ==========================================================
# COLOR THEME & CONFIGURATION
# ==========================================================
# These colors are used to make the GUI look clean and consistent.
BG_COLOR = "#F8FAFC"        # Light slate background
CARD_BG = "#FFFFFF"         # White card containers
TEXT_COLOR = "#0F172A"      # Deep slate text
MUTED_TEXT = "#64748B"      # Subdued gray text
BORDER_COLOR = "#CBD5E1"    # Subtle borders
PRIMARY_BTN = "#2563EB"     # Royal blue action button
PRIMARY_HOVER = "#1D4ED8"   # Darker blue on hover
SUCCESS_COLOR = "#16A34A"   # Green status
ERROR_COLOR = "#DC2626"     # Red status

# Create the main window for the application
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("760x760")
root.minsize(760, 760)
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Micro-interaction helper for hover states
# This changes the button color when the mouse enters or leaves it.
def on_btn_enter(event):
    event.widget.config(bg=PRIMARY_HOVER)

def on_btn_leave(event):
    event.widget.config(bg=PRIMARY_BTN)


# ==========================================================
# HEADER
# ==========================================================
# Title and subtitle at the top of the application
title_label = tk.Label(
    root,
    text="Steganography Tool",
    font=("Segoe UI", 20, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=(20, 4))

info_label = tk.Label(
    root,
    text="Conceal and recover arbitrary binary payloads using 24-bit LSB substitution",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=MUTED_TEXT
)
info_label.pack(pady=(0, 15))


# ==========================================================
# HIDE FILE SECTION (CARD 1)
# ==========================================================
# This frame contains all controls for hiding a secret file inside an image.
hide_frame = tk.LabelFrame(
    root,
    text=" Hide File Payload ",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    padx=20,
    pady=15
)
hide_frame.pack(padx=35, pady=8, fill="x")

# --- Row 0: Cover Image ---
# Label and entry field for selecting the cover image.
tk.Label(
    hide_frame, text="Cover Image:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR
).grid(row=0, column=0, sticky="w", pady=4)

cover_entry = tk.Entry(
    hide_frame, width=54, font=("Segoe UI", 9), relief="solid", bd=1
)
cover_entry.grid(row=0, column=1, padx=10)

def select_cover_image():
    # Open a file dialog to choose the image that will carry the hidden file
    file_path = filedialog.askopenfilename(
        title="Select Cover Image",
        filetypes=[
            ("PNG Images", "*.png"),
            ("JPEG Images", "*.jpg;*.jpeg"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        cover_entry.delete(0, tk.END)
        cover_entry.insert(0, file_path)

        # Show the file size to the user as a quick confirmation
        try:
            size_bytes = os.path.getsize(file_path)
            cover_info_label.config(
                text=f"Selected: {os.path.basename(file_path)}  |  Size: {size_bytes:,} bytes",
                fg="#0284C7"
            )
        except Exception:
            cover_info_label.config(text="")

tk.Button(
    hide_frame, text="Browse...", font=("Segoe UI", 9), bg="#F1F5F9", fg=TEXT_COLOR,
    relief="solid", bd=1, cursor="hand2", padx=8, pady=2, command=select_cover_image
).grid(row=0, column=2)

cover_info_label = tk.Label(
    hide_frame, text="", font=("Segoe UI", 8, "italic"), bg=CARD_BG, fg=MUTED_TEXT
)
cover_info_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 4))


# --- Row 2: Secret File ---
# This lets the user choose the file that will be hidden in the image.
tk.Label(
    hide_frame, text="Secret File:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR
).grid(row=2, column=0, sticky="w", pady=4)

secret_entry = tk.Entry(
    hide_frame, width=54, font=("Segoe UI", 9), relief="solid", bd=1
)
secret_entry.grid(row=2, column=1, padx=10)

def select_secret_file():
    # Ask for the file to hide
    file_path = filedialog.askopenfilename(
        title="Select Secret File",
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("PDF Documents", "*.pdf"),
            ("Word Documents", "*.docx;*.doc"),
            ("Images", "*.jpg;*.png;*.jpeg")
        ]
    )
    if file_path:
        secret_entry.delete(0, tk.END)
        secret_entry.insert(0, file_path)

        # Show file details so the user knows what was selected
        try:
            size_bytes = os.path.getsize(file_path)
            ext = os.path.splitext(file_path)[1].upper()
            secret_info_label.config(
                text=f"Selected: {os.path.basename(file_path)}  |  Format: {ext}  |  Size: {size_bytes:,} bytes",
                fg="#0284C7"
            )
        except Exception:
            secret_info_label.config(text="")

tk.Button(
    hide_frame, text="Browse...", font=("Segoe UI", 9), bg="#F1F5F9", fg=TEXT_COLOR,
    relief="solid", bd=1, cursor="hand2", padx=8, pady=2, command=select_secret_file
).grid(row=2, column=2)

secret_info_label = tk.Label(
    hide_frame, text="", font=("Segoe UI", 8, "italic"), bg=CARD_BG, fg=MUTED_TEXT
)
secret_info_label.grid(row=3, column=1, sticky="w", padx=10, pady=(0, 4))


# --- Row 4: Output Image ---
# This is the stego-image that will be created after hiding data.
tk.Label(
    hide_frame, text="Output Image:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR
).grid(row=4, column=0, sticky="w", pady=4)

output_entry = tk.Entry(
    hide_frame, width=54, font=("Segoe UI", 9), relief="solid", bd=1
)
output_entry.grid(row=4, column=1, padx=10)

def select_output_image():
    # Ask where to save the final stego image
    file_path = filedialog.asksaveasfilename(
        title="Save Stego Image",
        defaultextension=".png",
        filetypes=[("PNG Images", "*.png")]
    )
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

tk.Button(
    hide_frame, text="Browse...", font=("Segoe UI", 9), bg="#F1F5F9", fg=TEXT_COLOR,
    relief="solid", bd=1, cursor="hand2", padx=8, pady=2, command=select_output_image
).grid(row=4, column=2)


# --- Action: Hide File ---
# When the user clicks this button, the program hides the secret file in the image.
def run_hide_file():
    # Read values from the input fields
    cover_img = cover_entry.get()
    secret_f = secret_entry.get()
    out_img = output_entry.get()

    # Validate that the user entered all required information
    if not cover_img or not secret_f or not out_img:
        messagebox.showwarning("Missing Information", "Please select cover image, secret file, and output path.")
        return

    try:
        # Update the status label before carrying out the embedding
        status_label.config(text="Status: Embedding payload into image...", fg="#0284C7")
        root.update_idletasks()

        # Call the actual hiding function
        hide_file(cover_img, secret_f, out_img)

        # Show success message when the operation completes
        status_label.config(text="Status: Secret file hidden successfully!", fg=SUCCESS_COLOR)
        messagebox.showinfo("Success", "Secret file hidden into stego image successfully!")
    except Exception as error:
        # Handle errors and show a message to the user
        status_label.config(text="Status: Embedding failed.", fg=ERROR_COLOR)
        messagebox.showerror("Error", f"An error occurred:\n\n{error}")

hide_button = tk.Button(
    hide_frame,
    text="HIDE FILE",
    font=("Segoe UI", 10, "bold"),
    bg=PRIMARY_BTN,
    fg="#FFFFFF",
    activebackground=PRIMARY_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    width=20,
    pady=6,
    command=run_hide_file
)
hide_button.grid(row=5, column=1, pady=(12, 4))
hide_button.bind("<Enter>", on_btn_enter)
hide_button.bind("<Leave>", on_btn_leave)


# ==========================================================
# EXTRACT FILE SECTION (CARD 2)
# ==========================================================
# This frame contains controls for extracting the hidden file from a stego image.
extract_frame = tk.LabelFrame(
    root,
    text=" Extract File Payload ",
    font=("Segoe UI", 11, "bold"),
    bg=CARD_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    padx=20,
    pady=15
)
extract_frame.pack(padx=35, pady=8, fill="x")

# --- Row 0: Stego Image ---
# Select the image that contains hidden data.
tk.Label(
    extract_frame, text="Stego Image:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR
).grid(row=0, column=0, sticky="w", pady=4)

stego_entry = tk.Entry(
    extract_frame, width=54, font=("Segoe UI", 9), relief="solid", bd=1
)
stego_entry.grid(row=0, column=1, padx=10)

def select_stego_image():
    # Open a dialog to select the stego image
    file_path = filedialog.askopenfilename(
        title="Select Stego Image",
        filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")]
    )
    if file_path:
        stego_entry.delete(0, tk.END)
        stego_entry.insert(0, file_path)

        # Show file size for confirmation
        try:
            size_bytes = os.path.getsize(file_path)
            stego_info_label.config(
                text=f"Selected Stego: {os.path.basename(file_path)}  |  Size: {size_bytes:,} bytes",
                fg="#0284C7"
            )
        except Exception:
            stego_info_label.config(text="")

tk.Button(
    extract_frame, text="Browse...", font=("Segoe UI", 9), bg="#F1F5F9", fg=TEXT_COLOR,
    relief="solid", bd=1, cursor="hand2", padx=8, pady=2, command=select_stego_image
).grid(row=0, column=2)

stego_info_label = tk.Label(
    extract_frame, text="", font=("Segoe UI", 8, "italic"), bg=CARD_BG, fg=MUTED_TEXT
)
stego_info_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 4))


# --- Row 2: Output Directory ---
# Choose the folder in which the extracted file should be saved.
tk.Label(
    extract_frame, text="Output Folder:", font=("Segoe UI", 9, "bold"), bg=CARD_BG, fg=TEXT_COLOR
).grid(row=2, column=0, sticky="w", pady=4)

extract_output_entry = tk.Entry(
    extract_frame, width=54, font=("Segoe UI", 9), relief="solid", bd=1
)
extract_output_entry.grid(row=2, column=1, padx=10)

def select_extract_output():
    # Ask the user to choose a folder for the extracted file
    folder_path = filedialog.askdirectory(title="Select Output Directory")
    if folder_path:
        extract_output_entry.delete(0, tk.END)
        extract_output_entry.insert(0, folder_path)

tk.Button(
    extract_frame, text="Browse...", font=("Segoe UI", 9), bg="#F1F5F9", fg=TEXT_COLOR,
    relief="solid", bd=1, cursor="hand2", padx=8, pady=2, command=select_extract_output
).grid(row=2, column=2)


# --- Action: Extract File ---
# Run the extraction process when the button is clicked.
def run_extract_file():
    stego_img = stego_entry.get()
    out_dir = extract_output_entry.get()

    # Validate the user input
    if not stego_img or not out_dir:
        messagebox.showwarning("Missing Information", "Please select stego image and output destination folder.")
        return

    try:
        # Update the status before extraction starts
        status_label.config(text="Status: Extracting payload...", fg="#0284C7")
        root.update_idletasks()

        # Call the extraction function
        extract_file(stego_img, out_dir)

        # Show that the process completed successfully
        status_label.config(text="Status: Extraction completed successfully!", fg=SUCCESS_COLOR)
        messagebox.showinfo("Success", "Secret file extracted successfully!")
    except Exception as error:
        # Show any extraction errors
        status_label.config(text="Status: Extraction failed.", fg=ERROR_COLOR)
        messagebox.showerror("Error", f"An error occurred:\n\n{error}")

extract_button = tk.Button(
    extract_frame,
    text="EXTRACT FILE",
    font=("Segoe UI", 10, "bold"),
    bg=PRIMARY_BTN,
    fg="#FFFFFF",
    activebackground=PRIMARY_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    width=20,
    pady=6,
    command=run_extract_file
)
extract_button.grid(row=3, column=1, pady=(12, 4))
extract_button.bind("<Enter>", on_btn_enter)
extract_button.bind("<Leave>", on_btn_leave)


# ==========================================================
# STATUS BAR & FOOTER
# ==========================================================
# This status bar provides a simple message to the user at the bottom.
status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI", 9, "bold"),
    bg=BG_COLOR,
    fg=MUTED_TEXT,
    padx=10,
    pady=8
)
status_label.pack(padx=35, pady=(4, 6), fill="x")

# Exit button for closing the program
exit_button = tk.Button(
    root,
    text="Exit Tool",
    font=("Segoe UI", 9),
    bg="#E2E8F0",
    fg=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=14,
    pady=4,
    command=root.destroy
)
exit_button.pack(pady=(0, 15))

# Start the Tkinter event loop
root.mainloop()