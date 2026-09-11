from PIL import Image  # Pillow library for use to work with images
import os # To work with file paths and directories


def hide_file(cover_image_path, secret_file_path, output_image_path):
    image = Image.open(cover_image_path)
    image = image.convert('RGB')  # Ensure the image is in RGB mode

    # Read the secret file and get its size
    with open(secret_file_path, 'rb') as file: # Open the secret file in binary mode 'rb, 'rb' allow us to read the file as bytes, which is necessary for hiding binary data in the image.
        secret_data = file.read()

    # Add metadata to the secret data
    filename = secret_file_path.split("\\")[-1].split("/")[-1]
    filename_bytes = filename.encode("utf-8") # File name is converted to bytes using UTF-8 encoding, which allows us to store the filename in the image as well.
    file_size = len(secret_data)

    print("--- Hiding Process ---\n")

    print("Secret File Information:")
    print(f"[DEBUG] Secret filename: {filename}")
    print(f"[DEBUG] Secret file size: {file_size} bytes")
    print(f"[DEBUG] First 20 secret bytes: {secret_data[:20]}\n")

    # Hidden payload structure: [header][filename length][file size][filename][secret data]
    header = b"STEG"

    payload = (
        header
            + len(filename_bytes).to_bytes(2, "big")
            + file_size.to_bytes(8, "big")
            + filename_bytes
            + secret_data
    )

    print("Payload Information:")
    print(f"[DEBUG] Payload size: {len(payload)} bytes")
    print(f"[DEBUG] Header: {payload[:4]}")
    print(f"[DEBUG] Filename length bytes: {payload[4:6]}")
    print(f"[DEBUG] File size bytes: {payload[6:14]}")
    print(f"[DEBUG] Payload first 30 bytes: {payload[:30]}\n")

    # Convert the payload to a bits
    bits = []
    for byte in payload: # loop break bits into line by line
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    # Get the image pixels
    pixels = list(image.getdata()) # Get the pixel data from the image and convert it to a list of tuples, where each tuple represents the RGB values of a pixel.

    # check the capacity of the image to hide the payload
    capacity = len(pixels) * 3 # Because each pixel has 3 color channels (R, G, B), the total number of bits that can be hidden in the image is equal to the number of pixels multiplied by 3
    if len(bits) > capacity:
        raise ValueError("Secret file is too large for the cover image.") # If the secret is too big, the program will stop rather than corrupting the image.

    # Modify the LSB (Steganography)
    # Embed bits into pixel LSBs
    new_pixels = []
    bit_index = 0

    print("Embedding Information:")
    print(f"[DEBUG] Total bits to embed: {len(bits)}")
    print(f"[DEBUG] Image capacity: {capacity} bits")

    # Loop through each pixel in the image and modify its LSB to hide the secret data. The LSB of each color channel (R, G, B) is modified to store one bit of the secret data at a time.
    # If there are no more bits to hide, the original pixel value is retained.
    # This is the algorithm that hides the secret data in the image using LSB steganography.
    for pixel in pixels:
        new_pixel = []

        for channel in pixel:
            value = channel

            if bit_index < len(bits):
                value = (value & 0xFE) | bits[bit_index]
                bit_index += 1

            new_pixel.append(value)

        new_pixels.append(tuple(new_pixel))

    print(f"[DEBUG] Bits actually embedded: {bit_index}\n")

    # Modify pixels back to the image
    image.putdata(new_pixels)

    # Save the modified image
    image.save(output_image_path, "PNG")

    print("Path Information:")
    print(f"Stego image saved to '{output_image_path}'")
    print(f"Secret file '{filename}' hidden in '{output_image_path}' successfully.\n")

    print("--- Hiding Process Completed ---\n")


def extract_file(stego_image_path, output_directory):

    # Load the stego image and convert it to RGB mode to ensure that we can access the pixel data correctly.
    image = Image.open(stego_image_path)
    image = image.convert("RGB")

    # get image pixels
    pixels = list(image.getdata())

    # extract the bits (LSB)
    bits = []

    print("--- Extraction Process ---\n")

    print("Stego Image Information:")
    print(f"[DEBUG] Number of pixels: {len(pixels)}")
    print(f"[DEBUG] Maximum extractable bits: {len(pixels) * 3}\n")

    for pixel in pixels:
        for channel in pixel:
            bits.append(channel & 1)

    # convert the bits back to bytes
    data = bytearray()

    for i in range(0, len(bits) - 7, 8):
        byte = 0

        for bit in bits[i:i + 8]:
            byte = (byte << 1) | bit

        data.append(byte)

    # Check that enough data exists for the header

    print("Extracted Data Information:")
    print(f"[DEBUG] Extracted total bytes: {len(data)}")
    print(f"[DEBUG] First 30 extracted bytes: {data[:30]}")

    if len(data) < 14:
        raise ValueError("The image does not contain enough hidden data.")

    print(f"[DEBUG] Extracted header: {data[:4]}\n")

    # Check for the header to ensure that the image contains hidden data.
    if data[:4] != b"STEG":
        raise ValueError("No valid hidden data found in this image.")

    # Read the filename length
    filename_length = int.from_bytes(data[4:6], "big")

    # Read the file size
    file_size = int.from_bytes(data[6:14], "big")

    print("Extracted Metadata Information:")
    print(f"[DEBUG] Extracted filename length: {filename_length}")
    print(f"[DEBUG] Extracted file size: {file_size}")

    # Extract the filename
    filename_start = 14
    filename_end = filename_start + filename_length

    if filename_end > len(data):
        raise ValueError("Invalid filename information.")

    filename = data[filename_start:filename_end].decode("utf-8") # Decode the filename from bytes to a string using UTF-8 encoding, which allows us to retrieve the original filename of the hidden file.

    print(f"[DEBUG] Extracted filename: {filename}\n")

    # Extract the secret file data
    secret_data_start = filename_end
    secret_data_end = secret_data_start + file_size

    if secret_data_end > len(data):
        raise ValueError("The hidden file data is incomplete.")

    secret_data = data[secret_data_start:secret_data_end]

    print("Extracted Secret Data Information:")
    print(f"[DEBUG] Extracted secret data length: {len(secret_data)}")
    print(f"[DEBUG] First 20 extracted secret bytes: {secret_data[:20]}\n")

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Save extracted secret file
    output_path = os.path.join(output_directory, filename)

    with open(output_path, "wb") as file:
        file.write(secret_data)

    # Print the extracted filename, the size of bytes, and the output path

    print("Extraction Summary:")
    print(f"Extracted filename: {filename}")
    print(f"Extracted bytes: {len(secret_data)}")
    print(f"File successfully extracted to {output_path}")

    print("\n--- Extraction Process Completed ---\n")