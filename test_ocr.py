import cv2
import easyocr
import re

from test_database import lookup_card
from excel_database import save_card


# Initialize EasyOCR once
reader = easyocr.Reader(['en'], gpu=False)


def scan_card(image_path):

    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not find {image_path}")

    # Get image dimensions
    height, width = image.shape[:2]

    # Crop the Pokemon name
    name_image = image[
        int(height * 0.055):int(height * 0.11),
        int(width * 0.25):int(width * 0.55)
    ]

    # Crop the collector number
    number_image = image[
        int(height * 0.93):height,
        int(width * 0.78):width
    ]

    # Read text
    names = reader.readtext(name_image, detail=0)
    numbers = reader.readtext(number_image, detail=0)

    # Get Pokemon name
    pokemon_name = names[0] if names else "Unknown"

    # Get card number
    card_number = "Unknown"

    for text in numbers:
        match = re.search(r"\d+\s*/\s*\d+", text)

        if match:
            card_number = match.group()
            break

    print("Pokemon name:", pokemon_name)
    print("Card number:", card_number)

    # Look up the card
    if pokemon_name != "Unknown" and card_number != "Unknown":

        card = lookup_card(pokemon_name, card_number)

        if card:
            print("\nDatabase match found!")
            print("Pokemon:", card["name"])
            print("Set:", card["set"]["name"])
            print("Rarity:", card.get("rarity", "Unknown"))
            print("HP:", card.get("hp", "Unknown"))

            # Save the card to Excel
            save_card(card, card_number, image_path)

            return card

        else:
            print("No matching card found.")

    else:
        print("Could not read the Pokemon name or number.")

    return None


# Run a test when this file is executed directly
if __name__ == "__main__":
    scan_card("images/kabuto.jpg")