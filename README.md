# Image Steganography & Steganalysis Tool

A Python-based desktop application developed for **IKB21303 Data Hiding & Encryption** (Assignment 2) at Universiti Kuala Lumpur (UniKL MIIT).

## Features
- **Spatial Domain LSB Substitution:** Embeds arbitrary binary files into PNG cover images.
- **Multi-Format Support:** Successfully hides and extracts `.txt`, `.pdf`, and `.jpg` payloads without corruption.
- **Dynamic 14-Byte Header:** Embeds `STEG` magic signature, filename length, and 64-bit payload size.
- **Steganalysis Module:** Generates 256-bin RGB histograms and checks pixel-level differences.
- **Dual GUI:** Dedicated Tkinter interfaces for hiding/extracting and steganalysis with image previews.

## Project Structure
- `steganography.py`: Core bitwise LSB embedding and extraction logic.
- `analysis.py`: Steganalysis, file size comparison, and RGB histogram generation.
- `gui_hide_extract.py`: GUI for hiding and extracting secret files.
- `gui_analysis.py`: GUI for running steganalysis with live previews.
- `main.py`: Automated CLI verification script.

## How to Run
1. Install dependencies:
   ```bash
   pip install pillow matplotlib numpy
   