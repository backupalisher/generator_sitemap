import pandas as pd
from os import listdir
import datetime
from jinja2 import Template
# import gzip


def save_main_sitemap():
    ignore_name = ['sitemap.xml']
    results = list(set(listdir("site")) - set(ignore_name))
    new_df = gen_sitemap(results)

    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                {% for page in pages %}
                <url>
                    <loc>{{page[1]|safe}}</loc>
                    <lastmod>{{page[3]}}</lastmod>
                    <changefreq>{{page[4]}}</changefreq>
                    <priority>{{page[5]}}</priority>
                </url>
                {% endfor %}
            </urlset>'''

    template = Template(sitemap_template)
    lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')

    for i in new_df:
        i.loc[:, 'lastmod'] = lastmod_date
        i.loc[:, 'changefreq'] = 'daily'
        i.loc[:, 'priority'] = '1.0'
        sitemap_output = template.render(pages=i.itertuples())
        # /var/www/part4_project/
        filename = '/var/www/part4_project/sitemap.xml'

        with open(filename, 'wt') as f:
            f.write(sitemap_output)


def save_sitemap(file_name, list_of_urls):
    new_df = gen_sitemap(list_of_urls)

    sitemap_template = '''<?xml version="1.0" encoding="UTF-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                {% for page in pages %}
                <url>
                    <loc>{{page[1]|safe}}</loc>
                </url>
                {% endfor %}
            </urlset>'''

    template = Template(sitemap_template)

    for i in new_df:
        sitemap_output = template.render(pages=i.itertuples())
        # filename = file_name + str(i.iloc[0, 1]) + '.xml.gz'
        filename = '/var/www/part4_project/' + file_name + str(i.iloc[0, 1]) + '.xml'
        # with gzip.open(filename, 'wt') as f:
        with open(filename, 'wt') as f:
            f.write(sitemap_output)


def gen_sitemap(list_of_urls):
    list_of_urls = pd.DataFrame(list_of_urls)

    special_char = {'&': '&', '\'': '\'', '\"': '\"', '>': '&gt', '<': '<'}
    list_of_urls[0] = list_of_urls[0].replace(special_char, regex=True)

    n = 50000

    list_of_urls.loc[:, 'name'] = ''

    new_df = [list_of_urls[i:i + n] for i in range(0, list_of_urls.shape[0], n)]

    for i, v in enumerate(new_df):
        v.loc[:, 'name'] = str(v.iloc[0, 1]) + '_' + str(i)

    return new_df
