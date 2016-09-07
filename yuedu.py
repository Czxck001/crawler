''' Crawler to grab articles and recitations from yuedu.fm
'''
import os
import re
import requests

import argparse
parser = argparse.ArgumentParser('yuedu.fm Crawler')
# parser.add_argument('-c', '--channels', type=int, nargs='*',
#                     help='Channel indexes')
# parser.add_argument('-p', '--max_page', type=int,
#                     help='Max page index')
parser.add_argument('-a', '--articles', type=int, nargs='*',
                    help='Artical indexes')
parser.add_argument('-m', '--max_article', type=int, default=0,
                    help='Max Artical index')
parser.add_argument('-o', '--output_dir',
                    help='Output Folder Directory')

FLAGS = parser.parse_args()

root = r'http://yuedu.fm'
channel_root = root + r'/channel/'
article_root = root + r'/article/'

# def list_page(page_url):
#     ''' Parse the html of a list page and return indexes of the articles
#     '''
#     html = requests.get(page_url).text
#     results = re.findall(
#         r'<a href="/article/([0-9]*)/"><img src="', html)
#     return results


def article_page(page_url):
    ''' Return article text and recitation audio url
    '''
    html = requests.get(page_url).text

    finding = re.findall(r'<div class="not-found">', html)
    if finding:  # page not found
        return None, None

    finding = re.findall(
        r'<span class="item-intro-hide"></span>'
        r'([\S\s]*)'
        r'</div>[\s]*<a href="javascript:;" class="item-intro-more fr">',
        html)
    if not finding:
        raise RuntimeError('Article Content Not Found')

    raw_article = finding[0]

    # remove html tags
    raw_article = re.sub(r'<[A-Za-z0-9/\-=":;\.\! ]*>', '', raw_article)

    lines = [line
             .replace(r'&gt;', '>')
             .replace(r'&lt;', '<')
             .replace(r'&igrave;', 'ì')
             .replace(r'&aacute;', 'á')
             .replace(r'&agrave;', 'à')
             .replace(r'&eacute;', 'é')
             .replace(r'&oacute;', 'ó')
             .replace(r'&bdquo;', '„')
             .replace(r'&not;', '¬')
             .replace(r'&bull;', '•')
             .replace(r'&amp;', '&')
             .replace(r'&ndash;', '–')
             .replace(r'&times;', '×')
             .replace(r'&#39;', "'")
             .replace(r'&middot;', '·')
             .replace(r'&quot;', '"')
             .replace(r'&lsquo;', '‘')
             .replace(r'&rsquo;', '’')
             .replace(r'&ldquo;', '“')
             .replace(r'&rdquo;', '”')
             .replace(r'&hellip;', '…')
             .replace(r'&mdash;', '—')
             .replace(r'&nbsp;', ' ')
             .strip()
             for line in raw_article.split('<br />')]

    article = '\n'.join('\n'.join(lines).split('\n'))

    # check if there is something left
    html_annotations = re.findall(r'(&.*;)', article) +\
        re.findall(r'<(.*)>', article)
    if html_annotations:
        print(page_url, html_annotations)

    finding = re.findall(r'mp3:"(.*)"', html)
    if not finding:
        raise RuntimeError('Recitation Audio Not Found')
    mp3_url = finding[0]

    return article, mp3_url

# article, mp3_url = article_page(article_root + '%d/' % 447)
# print(article)
# exit()

if FLAGS.max_article > 0:
    indexes = range(1, FLAGS.max_article + 1)
else:
    indexes = FLAGS.articles

N = len(indexes)


if not os.path.isdir(FLAGS.output_dir):
    os.mkdir(FLAGS.output_dir)

for k, i in enumerate(indexes):
    article, mp3_url = article_page(article_root + '%d/' % i)

    if not article or not mp3_url:
        print('Page Not Found at article %d' % i)
        continue

    with open(os.path.join(FLAGS.output_dir, '%d.txt' % i), 'w') as f:
        f.write(article)
    with open(os.path.join(FLAGS.output_dir, '%d.url' % i), 'w') as f:
        f.write(root + mp3_url)
    print(k + 1, '/', N, end='\r')
