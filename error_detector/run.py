import pytesseract
import cv2
import os
import re

stop_codes = {
    "CRITICAL PROCESS DIED": "0x000000EF: This indicates that a critical system process died.",
    "APC INDEX MISMATCH": "0x00000001: This indicates that there has been a mismatch in the APC state index.",
    "DEVICE QUEUE NOT BUSY": "0x00000002: Indicates that a device queue was not busy.",
    "IRQL NOT LESS OR EQUAL": "0x0000000A: This indicates that a kernel-mode driver attempted to access pageable memory at a high IRQL.",
    "KMODE EXCEPTION NOT HANDLED": "0x0000001E: This indicates that a kernel-mode program generated an exception which the error handler did not catch.",
    "SYSTEM SERVICE EXCEPTION": "0x0000003B: This indicates that an exception happened while executing a routine that transitions from non-privileged code to privileged code.",
    "PAGE FAULT IN NONPAGED AREA": "0x00000050: This indicates that invalid system memory has been referenced.",
    "SYSTEM THREAD EXCEPTION NOT HANDLED": "0x0000007E: This indicates that a system thread generated an exception that the error handler did not catch.",
    "UNEXPECTED KERNEL MODE TRAP": "0x0000007F: This indicates that the Intel CPU generated a trap and the kernel failed to catch this trap.",
    "DRIVER IRQL NOT LESS OR EQUAL": "0x000000D1: This indicates that a kernel-mode driver attempted to access pageable memory at a high IRQL."
}

image_directory = '~/My_Project/error_detector/image_storage'
image_directory = os.path.expanduser(image_directory)

if not os.path.exists(image_directory):
    os.makedirs(image_directory)

def find_stop_code(text):
    match = re.search(r'Stop code:\s*([A-Z\s]+)', text)
    if match:
        return match.group(1).strip()
    return None

def process_images(directory):
    try:
        for filename in os.listdir(directory):
            if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                image_path = os.path.join(directory, filename)
                print(f"Processing file: {filename}")  # Debugging message
                
                img = cv2.imread(image_path)

                if img is None:
                    print(f"Error reading image {filename}.")
                    continue

                text = pytesseract.image_to_string(img)

                print(f"OCR Text from {filename}:")
                print(text)
                print("--------------")
                
                stop_code = find_stop_code(text)
                if stop_code and stop_code in stop_codes:
                    print(f"Stop Code found: {stop_code}")
                    print(f"Description: {stop_codes[stop_code]}")
                else:
                    print("No Stop Code found.")
                    
    except FileNotFoundError as e:
        error_code = e.errno
        print(f"Error: {stop_codes.get(f'0x{error_code:08X}', 'Unknown error')}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

process_images(image_directory)
