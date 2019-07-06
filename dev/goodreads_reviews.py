"""Get reviews from https://www.goodreads.com and transform it to Hugo templates"""

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

# https://makina-corpus.com/blog/metier/2016/the-worlds-simplest-python-template-engine
TEMPLATE = '''
+++
title = "{review.book_title}"
description = "{review.review_text}"
date = "{review.read_date_text}"
+++
'''


@dataclasses.dataclass
class Review:
    book_title: str
    author_names: str
    my_rating: str
    review_text: str
    image_url: str
    read_date_text: str


class DataclassesJSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get reviews from https://www.goodreads.com and transform it to Hugo templates"
        )
    parser.add_argument("-k", "--key", help="Goodreads API key", nargs='?')
    args = parser.parse_args()

    key: str = args.key
    if key is None:
        print("Key is not specified. Unnable to load reviews.")
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
    link_pattern = re.compile(r'(\d+)m/(\d+.jpg)')

    root: ET.Element = ET.fromstring(response_str)
    reviews: List[Review] = []
    review: ET.Element
    for review in root.iter('review'):
        book: ET.Element = review.find('book')

        book_title: str = book.find('title').text
        author_names: str = ', '.join([a.find('name').text for a in book.iter('author')])
        my_rating: str = review.find('rating').text
        review_text: str = (
            review.find('body').text
            .replace('<br />', '\n')
            .strip())
        image_url: str = book.find('image_url').text
        if '/nophoto/' in image_url:
            # print('INFO: No photo for “{}”, {}'.format(book_title, book.find('link').text))
            large_image_url: str = image_url
        else:
            large_image_url: str = link_pattern.sub(r'\1l/\2', image_url)

        read_date_element: ET.Element = review.find('read_at') or review.find('date_added')
        # Example: Wed Dec 12 11:05:48 -0800 2018
        read_date: datetime = datetime.strptime(read_date_element.text, '%a %b %d %H:%M:%S %z %Y')
        # Example: 2015-11-03T13:10:07+0300
        read_date_text = read_date.strftime('%Y-%m-%dT%H:%M:%S%z')

        reviews.append(Review(book_title, author_names, my_rating, review_text, image_url, read_date_text))

    with open('book-reviews.json', 'w') as file:
        json.dump(reviews, file, cls=DataclassesJSONEncoder, ensure_ascii=False, indent=2)

    print(
      TEMPLATE.format(review=reviews[0])
    )
