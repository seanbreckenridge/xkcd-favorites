#!/usr/bin/env python3

import os
import time
import json
import logging
from typing import List, Any, Dict, Tuple

import yaml
import requests
import backoff  # type: ignore[import]

root_dir: str = os.path.dirname(__file__)
favorites_file: str = os.path.join(root_dir, "favorites.yaml")  # source
data_file: str = os.path.join(root_dir, "data.json")  # output
xkcd_json_api: str = "http://xkcd.com/{}/info.0.json"

LOGLEVEL: str = os.environ.get("XKCD_LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s: %(message)s")


def get(url: str) -> requests.Response:
    time.sleep(1)
    return requests.get(url)


@backoff.on_exception(backoff.fibo, requests.exceptions.RequestException, max_tries=20)
def get_img_data(xkcd_id: int) -> Dict[str, str]:
    """Get image url from an xkcd id"""
    logging.info(f"Getting metadata for xkcd id: {xkcd_id}")
    resp: Dict[str, Any] = get(xkcd_json_api.format(xkcd_id)).json()
    return {"img_url": str(resp["img"])}


IDList = List[str]
JsonCache = Dict[str, Dict[str, str]]


def initialize_data() -> Tuple[IDList, JsonCache]:
    """Read from yaml/json files to get information about new ids/previous runs"""

    # get IDs from yaml file
    with open(favorites_file, "r") as f:
        ids: List[str] = list(map(str, yaml.load(f, Loader=yaml.FullLoader)))

    # read from data file (i.e. cached values) if it exists
    json_cache: JsonCache = {}
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                json_cache = json.load(f)
        except json.JSONDecodeError:
            logging.warning("JSON decode error reading 'data.json', re-creating cache.")
            pass

    # if id's from your favorites have been removed, remove them from the data dictionary:
    for xkcd_id in list(json_cache):
        if xkcd_id not in ids:
            logging.info(
                f"Couldn't find id: '{xkcd_id}' in favorites.yaml, removing from 'data.json'."
            )
            del json_cache[xkcd_id]

    return ids, json_cache


def main():
    ids, data = initialize_data()

    # if needed, download the information for an id.
    logging.debug(f"favorite id list: {ids}")
    logging.debug(f"cached ids: {(list(data.keys()))}")
    for xkcd_id in ids:
        if xkcd_id not in data:
            data[xkcd_id] = get_img_data(xkcd_id)
        else:
            logging.debug(f"Found information for id '{xkcd_id}' in 'data.json'")

    with open(data_file, "w") as f:
        f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
