import cv2
import numpy as np

def extract_and_crop_inside_red(image_path, output_path='extracted_zoomed.png'):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read the image.")
        return

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red regions
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No red-bordered regions found.")
        return

    # Pick the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a mask with the inside of the red contour
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

    # Extract the inside content with transparency
    bgr = cv2.bitwise_and(image, image, mask=mask)
    b, g, r = cv2.split(bgr)
    alpha = mask
    rgba = cv2.merge([b, g, r, alpha])

    # --- Crop to the bounding box of the filled region ---
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_rgba = rgba[y:y+h, x:x+w]

    # Save the zoomed-in region
    cv2.imwrite(output_path, cropped_rgba)
    print(f"Cropped and extracted content saved to {output_path}")

    # Optional: Show result
    cv2.imshow("Zoomed Extract", cropped_rgba)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
# extract_and_crop_inside_red("your_image.jpg")
