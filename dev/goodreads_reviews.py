"""Get reviews from https://www.goodreads.com and transform it to Hugo templates"""

import os
import sys
import argparse
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import re
import json
import dataclasses

from datetime import datetime
from typing import List
from unicodedata import normalize

# https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine
TEMPLATE = '''
+++
title = "{review.book_title}"
description = "{review.description}"
date = "{review.read_date_text}"

images = ["{review.image_url}"]  # for opengraph.html template, https://bit.ly/2V9KDX9

rating = {review.my_rating}
author_names = "{review.author_names}"
cover_url = "{review.image_url}"
+++

{review.review_text}
'''


@dataclasses.dataclass
class Review:
    book_title: str
    author_names: str
    my_rating: str
    description: str
    review_text: str
    image_url: str
    read_date_text: str


def transliterate_english_to_russian(original: str) -> str:
    symbols = (
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
        )
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return original.translate(tr)


def slug(text: str, encoding=None) -> str:
    clean_text: str = re.sub(r'[\W_]+', '-', text.strip()).strip('-')
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    slug: str = (
        normalize('NFKD', clean_text)
        .encode('ascii', 'ignore')
        .lower()
        .decode()
        )
    return slug


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get reviews from https://www.goodreads.com and transform it to Hugo templates"
        )
    parser.add_argument("-k", "--key", help="Goodreads API key", nargs='?')
    parser.add_argument("-p", "--path", help="Path to save reviews as hugo pages", nargs='?')
    args = parser.parse_args()

    key: str = args.key
    if key is None:
        print("Key is not specified. Unnable to load reviews.")
        sys.exit(1)
    path: str = args.path
    if path is None:
        print("Path is not specified. Unnable to save reviews.")
        sys.exit(1)
    if not os.path.exists(path):
        print("Path is not exists. Unnable to save reviews.")
        sys.exit(1)

    url = 'https://www.goodreads.com/review/list'
    parameters = {
        'v': 2,
        'key': key,
        'id': '27388779-anatoly-gladky',
        'shelf': 'read',
        'per_page': 200,
        }
    data: str = urllib.parse.urlencode(parameters).encode('ascii')
    with urllib.request.urlopen(url, data) as response:
        response_str: str = response.read().decode('utf-8')

    # example: https://images.gr-assets.com/books/1477845757m/27118836.jpg
    link_pattern = re.compile(r'(\S+)\._.{1,6}_(\.jpg)')

    root: ET.Element = ET.fromstring(response_str)
    reviews: List[Review] = []
    review_element: ET.Element
    for review_element in root.iter('review'):
        my_rating: str = review_element.find('rating').text
        if my_rating == '0':
            continue

        book_element: ET.Element = review_element.find('book')
        book_title: str = (
            book_element.find('title').text
            .replace('"', '\\"'))
        author_names: str = (
            ', '.join([a.find('name').text for a in book_element.iter('author')])
            .replace('"', '\\"'))

        review_text: str = (
            review_element.find('body').text
            .replace('<br />', '\n')
            .strip())
        multiple_reviews = review_text.split('---')
        if len(multiple_reviews) > 1:
            review_text = multiple_reviews[0].strip('\n')
        description: str = (
            review_text
            .replace('\n', ' ')
            .replace('"', '\\"'))

        image_url: str = book_element.find('image_url').text
        if '/nophoto/' in image_url:
            image_url = ''
        else:
            image_url = link_pattern.sub(r'\1\2', image_url)

        read_date_element: ET.Element = review_element.find('read_at') or review_element.find('date_added')
        # Example: Wed Dec 12 11:05:48 -0800 2018
        read_date: datetime = datetime.strptime(read_date_element.text, '%a %b %d %H:%M:%S %z %Y')
        # Example: 2015-11-03T13:10:07+0300
        read_date_text = read_date.strftime('%Y-%m-%dT%H:%M:%S%z')

        reviews.append(
            Review(book_title, author_names, my_rating, description, review_text, image_url, read_date_text)
            )

    review: Review
    for review in reviews:
        book_url: str = transliterate_english_to_russian(review.book_title)
        book_url = slug(book_url)
        article_path: path = os.path.join(path, book_url + '.md')

        with open(article_path, 'w') as file:
            file.write(TEMPLATE.format(review=review))
