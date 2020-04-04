import os
import time
import json
import logging
from io import BytesIO
from typing import Mapping, List, Any, Union

import yaml
import requests
import backoff  # type: ignore
from PIL import Image  # type: ignore

root_dir: str = os.path.dirname(__file__)
favorites_file: str = os.path.join(root_dir, "favorites.yaml")  # source
data_file: str = os.path.join(root_dir, "data.json")  # output
xkcd_json_api: str = "http://xkcd.com/{}/info.0.json"

LOGLEVEL: str = os.environ.get("XKCD_LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s: %(message)s")


def get(url) -> requests.Response:
    time.sleep(1)
    return requests.get(url)


@backoff.on_exception(backoff.fibo, requests.exceptions.RequestException, max_tries=20)
def get_img_data(id):
    """Get image url and height/width for the image for a xkcd id"""
    logging.info("Getting metadata for xkcd id: {}".format(id))
    # get metadata
    resp: Mapping[str, Any] = get(xkcd_json_api.format(id)).json()
    # get img dimensions
    img_obj: Image.Image = Image.open(BytesIO(get(resp["img"]).content))
    return {
        "img_url": resp["img"],
        "dimensions": {"height": img_obj.height, "width": img_obj.width},
    }


def initialize_data():
    """Read from yaml/json files to get information about new ids/previous runs"""

    # get IDs from yaml file
    with open(favorites_file, "r") as f:
        ids: List[str] = list(map(str, yaml.load(f, Loader=yaml.FullLoader)))

    # read from data file (i.e. cached values) if it exists
    json_cache: Mapping[str, Union[str, Mapping[str, int]]] = {}
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                json_cache = json.load(f)
        except json.JSONDecodeError:
            logging.warning("JSON decode error reading 'data.json', re-creating cache.")
            pass

    # if id's from your favorites have been removed, remove them from the data dictionary:
    for id in list(json_cache):
        if id not in ids:
            logging.info(
                f"Couldn't find id: '{id}' in favorites.yaml, removing from 'data.json'."
            )
            del json_cache[id]

    return ids, json_cache


def main():
    ids, data = initialize_data()  # type: ignore

    # if needed, download the information for an id.
    logging.debug("favorite id list: {}".format(ids))
    logging.debug("cached ids: {}".format(list(data.keys())))
    for id in ids:
        if id not in data:
            data[id] = get_img_data(id)
        else:
            logging.debug("Found information for id '{}' in 'data.json'".format(id))

    with open(data_file, "w") as f:
        f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
