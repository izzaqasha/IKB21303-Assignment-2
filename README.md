# Image Steganography & Steganalysis Tool

A Python-based desktop application developed for **IKB21303 Cryptography and Steganography** (Assignment 2) at Universiti Kuala Lumpur - Malaysian Institute of Information Technology (UniKL MIIT).

---

## Features

- **Spatial Domain LSB Substitution:** Embeds arbitrary binary data into 24-bit TrueColor PNG cover images without visible distortion[cite: 2, 3].
- **Dynamic 14-Byte Binary Protocol:** Uses a custom header structure (`STEG` magic signature + 2-byte filename length + 8-byte payload size) to preserve original filenames, extensions, and file sizes upon recovery[cite: 2, 3].
- **Multi-Format Support:** Successfully embeds and extracts multiple file types without corruption, including plain text (`.txt`), documents (`.pdf`), and images (`.jpg`)[cite: 1, 2, 3].
- **Steganalysis & Histogram Analysis:** Generates 256-bin RGB frequency histograms, computes pixel-level difference metrics, and evaluates PNG DEFLATE file size variations[cite: 2, 5].
- **Dual Graphical User Interface (Tkinter):**
  - Hiding & Extraction interface for seamless carrier and payload selection.
  - Steganalysis interface featuring real-time image preview thumbnails and an itemized statistical report popup.

---

## Project Structure

```text
IKB21303-Assignment-2/
│
├── cover_images/                  # Pristine carrier images (cover.png)
├── secret_files/                  # Payloads for hiding (secret.txt, secret.pdf, secret.jpg)
├── output/                        # Generated stego images, extracted payloads, and histogram charts
│   ├── extracted_txt/             # Recovered .txt files
│   ├── extracted_pdf/             # Recovered .pdf files
│   └── extracted_jpg/             # Recovered .jpg files
│
├── steganography.py               # Core bitwise LSB embedding and extraction algorithms
├── analysis.py                    # Steganalysis calculations, RGB histogram generation, and file size metrics
├── gui_hide_extract.py            # Desktop GUI for embedding and extraction operations
├── gui_analysis.py                # Desktop GUI for steganalysis with image preview thumbnails
├── main.py                        # Automated CLI script for testing the backend engine
├── .gitignore                     # Git exclusion rules for virtual environments and cache
└── README.md                      # Project documentation

. **Clone the repository:**
```bash
git clone [https://github.com/izzaqasha/IKB21303-Assignment-2.git](https://github.com/izzaqasha/IKB21303-Assignment-2.git)
cd IKB21303-Assignment-2
```

2. **Set up a Python virtual environment (Recommended):**
```bash
# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install required dependencies:**
```bash
pip install pillow matplotlib numpy
```