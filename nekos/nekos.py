import json
import requests
import random
from . import errors

def nsfwimg(endpoint: str):
    endpoints = ['solog', 'feet', 'lewdkemo', 'solo', 'cum', 'les', 'erokemo', 'bj', 'ero', 'hololewd',
                'tits', 'nsfw_neko_gif', 'eroyuri', 'holoero', 'pussy', 'yuri', 'hentai', 'feetg', 'eron', 'erok',
                'erofeet', 'blowjob', 'kuni', 'classic', 'femdom', 'boobs', 'trap', 'lewd', 'anal', 'futanari', 'lewdk', 'random']

    if endpoint.lower() not in endpoints:
        raise errors.InvalidArgument(f"That's not a valid category.\n\n**Categories**: \n{', '.join(endpoints)}")

    try:
        if endpoint == 'random':
            endpoint = random.choice(endpoints)
            url = 'https://nekos.life/api/v2/img/' + endpoint.lower()
        else:
            url = 'https://nekos.life/api/v2/img/' + endpoint.lower()
        r = requests.get(url).json()
        return(r['url'], endpoint.upper())
    except Exception as e:
        raise errors.NothingFound('Not able to contact the API')

def owoify(text: str):
    if len(text) not in range(1, 200):
        raise errors.EmptyArgument(f'The length of the text must be `1-200` characters.')

    try:
        url = 'https://nekos.life/api/v2/owoify?text=' + text
        r = requests.get(url).json()
        return(r["owo"])
    except Exception as e:
        raise errors.NothingFound('Not able to contact the API')