"""Dumping all the functions here for now
"""
import os
import shutil
import logging

import feedparser
import tarfile
import requests


_logger = logging.getLogger(__name__)


def get_arxiv_ids(url: str = "http://arxiv.org/rss/cond-mat.str-el"):
    feed = feedparser.parse(url)
    return [entry["id"].rsplit("/", 1)[-1] for entry in feed["entries"]]


def id_to_url(id: str):
    "URL to download the source file for a paper"
    return "http://arxiv.org/e-print/" + str(id)


def download_source(id, path="data"):
    url = id_to_url(id)
    path = os.path.join(path, id)

    r = requests.get(url, stream=True)

    if not os.path.exists(path):
        os.makedirs(path)

    filename = os.path.join(path, id + ".tar.gz")

    with open(filename, "wb") as f:
        f.write(r.content)


def extract_source(id, path="data"):
    path = os.path.join(path, id)
    tar = tarfile.open(os.path.join(path, id + ".tar.gz"))
    tar.extractall(path)
    tar.close()


def get_today(path):
    """Retrieve today's articles"""

    _logger.info("Getting today's article ids")
    ids = get_arxiv_ids()

    for id in ids:
        _logger.info(f"Downloading article {id}")
        download_source(id, path=path)
        _logger.info(f"Extracting source for article {id}")
        extract_source(id, path=path)
