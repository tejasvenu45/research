import os
import pytesseract
from PIL import Image, ImageFilter
import numpy as np
import cv2

def ocr_image(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def extract_multi_column_text(image_path):
    try:
        with Image.open(image_path) as img:
            grayscale_img = img.convert("L")
            full_text = pytesseract.image_to_string(grayscale_img)
            return full_text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def preprocess_image(image_path):
    try:
        with Image.open(image_path) as img:
            grayscale_img = img.convert("L")
            deskewed_img = deskew_image(grayscale_img)
            threshold = 150
            binary_img = deskewed_img.point(lambda p: p > threshold and 255)
            denoised_img = remove_noise(binary_img)
            return denoised_img
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def deskew_image(image):
    img_array = np.array(image)
    lines = cv2.HoughLines(img_array, 1, np.pi / 180, 200)
    skew_angle = 0
    if lines is not None:
        for rho, theta in lines[:, 0]:
            skew_angle += theta
    return image.rotate(-skew_angle / len(lines), resample=Image.BICUBIC, expand=True)

def remove_noise(image):
    return image.filter(ImageFilter.MedianFilter)

def process_image(image_path):
    preprocessed_img = preprocess_image(image_path)
    if preprocessed_img:
        full_text = ocr_image(image_path)
        return full_text if full_text else "No text extracted from the image."
    else:
        return "Error preprocessing the image."
    