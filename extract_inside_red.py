import os
import cv2
import numpy as np

def extract_and_crop_inside_red(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"[!] Could not read {image_path}")
        return False

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"[!] No red-bordered regions in {image_path}")
        return False

    largest_contour = max(contours, key=cv2.contourArea)

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

    bgr = cv2.bitwise_and(image, image, mask=mask)
    b, g, r = cv2.split(bgr)
    alpha = mask
    rgba = cv2.merge([b, g, r, alpha])

    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_rgba = rgba[y:y+h, x:x+w]

    cv2.imwrite(output_path, cropped_rgba)
    print(f"[✓] Saved: {output_path}")
    return True

def process_directory_recursively(root_folder="."):
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            name, ext = os.path.splitext(filename)
            if ext.lower() in image_extensions:
                output_name = f"cropped_{name}.png"
                output_path = os.path.join(dirpath, output_name)
                success = extract_and_crop_inside_red(filepath, output_path)
                if not success:
                    os.remove(filepath)
                    print(f"[✗] Deleted: {filepath}")

if __name__ == "__main__":
    process_directory_recursively()
