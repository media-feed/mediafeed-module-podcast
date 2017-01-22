#!/usr/bin/env python3

import sys
from datetime import datetime
from feedparser import parse
from hashlib import sha1
from mediafeed.modulehelper import ModuleProcess, run
from re import sub
from unicodedata import normalize


__version__ = '0.1.dev0'


def slugify(value):
    value = normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = sub(r'[^\w\s-]', '', value).strip().lower()
    return sub(r'[-\s]+', '-', value)


class ModulePodcast(ModuleProcess):
    def info(self):
        return {
            'name': 'Podcast',
            'media': 'audio',
            'description': 'Podcasts download',
        }

    def is_valid_url(self, url, options=None):
        return parse(url).bozo == 0

    def get_source_metadata(self, url, options=None):
        rss = parse(url)
        if rss.bozo != 0:
            raise Exception('Content of "%s" is not valid' % url)
        return {
            'id': slugify(rss.feed.title),
            'url': rss.href,
            'name': rss.feed.title,
            'thumbnail_url': rss.feed.image.href or None,
            'web_url': rss.feed.link or None,
        }

    def get_items(self, url, options=None):
        rss = parse(url)
        if rss.bozo != 0:
            raise Exception()
        for entry in rss.entries[::-1]:
            links = [link['url'] for link in entry.links
                     if link.get('rel') == 'enclosure' and link.get('url')]
            if not links:
                print('"%s" does not have media content' % entry.link, file=sys.stderr)
                continue
            time = entry.published_parsed
            yield {
                'id': sha1(entry.id.encode('utf-8')).hexdigest(),
                'url': entry.link,
                'timestamp': datetime(time.tm_year, time.tm_mon, time.tm_mday,
                                      time.tm_hour, time.tm_min, time.tm_sec).timestamp(),
                'name': entry.title,
                'media_url': links[0],
                'text': entry.summary,
            }


def main():
    run(ModulePodcast())


if __name__ == '__main__':
    main()
