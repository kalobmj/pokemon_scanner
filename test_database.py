import requests


def lookup_card(pokemon_name, card_number):

    number, total = card_number.split("/")

    url = "https://api.tcgdex.net/v2/en/cards"

    params = {"name": pokemon_name}

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    cards = response.json()

    for card in cards:

        if card["name"].lower() != pokemon_name.lower():
            continue

        if str(card["localId"]) != number:
            continue

        card_url = f"{url}/{card['id']}"

        details_response = requests.get(card_url, timeout=15)
        details_response.raise_for_status()

        details = details_response.json()

        set_info = details["set"]
        set_total = set_info["cardCount"]["official"]

        if str(set_total) != total:
            continue

        return details

    return None


# Only run this test when executing test_database.py directly
if __name__ == "__main__":

    card = lookup_card("Kabuto", "50/62")

    if card:
        print("Pokemon:", card["name"])
        print("Set:", card["set"]["name"])
        print("Rarity:", card.get("rarity", "Unknown"))
        print("HP:", card.get("hp", "Unknown"))
    else:
        print("Card not found.")