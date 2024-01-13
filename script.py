import requests
import json
import time

url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?format=tcg'

response = requests.get(url)

# print(response.json()['data'][0]['card_images'][0]['image_url'])

num_of_requests = 0
index = 1423
for card in response.json()['data'][1423:]:
    download_url = card['card_images'][0]['image_url_cropped']
    key = card['id']
    card_type = card['type']
    frame_type = card['frameType']
    if frame_type == 'skill':
        index = index + 1
        continue
    name = card['name']
    race = card['race']
    atk = card.get('atk', 0)
    defense = card.get('def', 0)
    level = card.get('level', 0)
    attribute = card.get('attribute', 'none')
    linkval = card.get('linkval', 'none')

    information = {
        'key': key,
        'name': name,
        'race': race,
        'atk': atk,
        'defense': defense,
        'level': level,
        'attribute': attribute,
        'linkval': linkval,
        'type': card_type,
        'frame_type': frame_type
    }

    image = requests.get(download_url)
    if response.status_code == 200:
        with open(f"images/{key}.jpg", 'wb') as file:
            file.write(image.content)
        with open(f"images/{key}.json", "w") as json_file:
            json.dump(information, json_file, indent=4)
        num_of_requests += 1
        if num_of_requests == 19:
            time.sleep(1)
            num_of_requests = 0
    index = index + 1

with open(f"index.json", "w") as json_file:
    json.dump(index, json_file, indent=4)

