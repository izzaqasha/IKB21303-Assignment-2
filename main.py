from steganography import hide_file, extract_file

# File paths
cover_image = "cover_images/cover.png"
secret_file = "secret_files/secret.txt"
stego_image = "output/stego.png"
extracted_folder = "output/extracted"

# Hide the secret file
hide_file(
    cover_image,
    secret_file,
    stego_image
)

# Extract the secret file
extract_file(
    stego_image,
    extracted_folder
)