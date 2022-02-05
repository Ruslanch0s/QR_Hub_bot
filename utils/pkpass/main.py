import json
from pathlib import Path

import aiohttp

from data.config import APP_KEY


async def get_pkpass(path_to_download: Path, url: str):
    new_url = url.split('?', 1)
    new_url.insert(1, '.pkpass?')
    url_to_download = "".join(new_url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_to_download, ssl=False) as response:
            print(response.status)
            with open(path_to_download, 'wb') as file:
                file.write(await response.read())
                file.close()


async def create_pkpass(text_for_generate: str, template_id: int):
    template_values = {'code': text_for_generate}
    kwargs = {}
    kwargs['data'] = json.dumps(template_values)
    headers = {
        'User-Agent': 'PassSlotSDK-Python/%s' % '1',
        'Accept': 'application/json, */*; q=0.01',
        'Authorization': APP_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.passslot.com/v1/templates/{template_id}/pass', headers=headers, **kwargs,
                                ssl=False) as response:
            data = await response.json()
            print(response.status)
            return data.get('url')
