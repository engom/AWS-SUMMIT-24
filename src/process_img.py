import os

import pyheif
from PIL import Image

# Directory containing  subdir with .HEIC files
root_dir = os.getcwd()  # os.path.join(os.getcwd(), "Text2SQL")

# Filter the list to only include directories
items = sorted(
    (f for f in os.listdir(root_dir) if not f.startswith(".")),
    key=str.lower,
)  # sorted(os.listdir(root_dir))
folders = [
    item
    for item in items
    if os.path.isdir(os.path.join(root_dir, item)) and item != "src"
]

for directory in folders:
    # Markdown file
    markdown_file = open(f"{directory}.md", "w")

    img_list = sorted(os.listdir(directory))
    print(f"Images in {directory} preview: {img_list[:5]}")

    for file_ in img_list:
        if file_.endswith(".HEIC") or file_.endswith(".heic"):
            filename = os.path.join(directory, file_)
            heif_file = pyheif.read(filename)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

            # Convert .HEIC to .jpg
            new_file = os.path.splitext(filename)[0] + ".jpg"
            image.save(new_file, format="JPEG")

            # Write image name to markdown file
            markdown_file.write(f"![{file_}]({new_file})\n")

    markdown_file.close()
