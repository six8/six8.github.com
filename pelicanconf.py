#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from os import path, walk

AUTHOR = u'Mike Thornton'
SITENAME = u'Dev Details'
SITEURL = 'http://devdetails.com'

TIMEZONE = 'America/Chicago'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  []
# Social widget

SOCIAL = []

GOOGLE_ANALYTICS = 'UA-27029635-1'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = False

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

DEFAULT_CATEGORY = 'Articles'

ARTICLE_DIR = 'articles'

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'

ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'

THEME = "./theme"

PLUGIN_PATH = 'plugins'
PLUGINS = ['assets']

WEBASSETS = True
ASSET_CONFIG = (
    ('less_bin', path.abspath("./node_modules/.bin/lessc")),
)

FEED_DOMAIN = SITEURL
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'

FILES_TO_COPY = [('../CNAME', 'CNAME')]

for (dirpath, dirnames, filenames) in walk('content/raw'):
    for filename in filenames:
        FILES_TO_COPY.append((
            path.join('raw', filename),
            filename
        ))