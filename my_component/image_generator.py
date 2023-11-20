import cv2
import json
from pathlib import Path

def generate_images_with_icons(numbers, output_path):
    # Load image and icon
    media_folder = Path(__file__).parent.parent / 'assets'
    image_path = media_folder / 'map1.png'
    icon_path = media_folder / 'icon.png'
    json_path = media_folder / 'coordinates.json'
    image = cv2.imread(str(image_path))
    icon = cv2.imread(str(icon_path), cv2.IMREAD_UNCHANGED)

    with open(json_path, 'r') as file:
        json_data = json.load(file)

    # Process each number and draw icons
    for num in numbers:
        print(f"Processing number: {num}")  # Debug print
        str_num = str(num)  # Convert number to string
        if str_num in json_data:
            coord = json_data[str_num]
            print(f"Drawing icon at: {coord}")  # Debug print
            draw_icon(image, (coord["x"], coord["y"]), icon)
        else:
            print(f"Number {num} not found in JSON data")  # Debug print

    # Save the image to the specified output path
    cv2.imwrite(output_path, image)

    return image

def draw_icon(image, position, icon=None):
    if icon is not None:
        icon_resized = cv2.resize(icon, (50, 50))  # Resize icon, adjust as needed
        x, y = position
        h, w, _ = icon_resized.shape

        # Blend icon with the image
        for i in range(h):
            for j in range(w):
                if icon_resized[i, j, 3] != 0:  # Check alpha channel
                    image[y + i, x + j] = icon_resized[i, j][:3]
    else:
        cv2.circle(image, position, 20, (0, 0, 255), -1)  # Draw a red dot
