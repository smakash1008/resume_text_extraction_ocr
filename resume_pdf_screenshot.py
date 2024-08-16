# Importing the Necessary Libraries:

import json
import os
import time
import re
import docx2txt
import google.generativeai as genai
import pdfminer
from pdfminer.high_level import extract_text
from google.api_core import retry
from dotenv import load_dotenv
load_dotenv()
from pdf2image import convert_from_path
import shutil
from PIL import Image

file_path = input("Enter the File Path and Name: ")

output_directory = 'Output_images1'
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)

os.makedirs(output_directory, exist_ok=True)

images = convert_from_path(file_path,poppler_path=os.getenv("poppler"), dpi=300)
for i, image in enumerate(images):
    filename = os.path.join(output_directory, f"Resume_Page_{i + 1}.png")
    image.save(filename, "PNG")
    print(f"{filename} Saved...")

widths, heights = zip(*(img.size for img in images))
print(widths, heights)

total_height = sum(heights)
max_width = max(widths)
print(total_height)
print(max_width)

combined_image = Image.new("RGB", (max_width,total_height))

y_offset = 0
for img in images:
    print(y_offset)
    combined_image.paste(img, (0, y_offset))
    y_offset += img.height

combined_image_path = os.path.join(output_directory, 'combined_image.png')
combined_image.save(combined_image_path, "PNG")
print(f"{combined_image_path} Saved...")

print("Successfully Completed...")