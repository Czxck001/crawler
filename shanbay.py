''' Crawler to grab wordlists from shanbay.com
'''
import os
import os.path as op
import json
import re
import argparse
import requests

root_url = r'https://www.shanbay.com'
list_pattern = re.compile(r'<td class=\"wordbook-wordlist-name\">'
                          r'[\s]*<a href=\"(.*)\">(.*)</a>[\s]*</td>')
word_pattern = re.compile(r'<td class="span2"><strong>(.*)</strong></td>')
word_explanation_pattern = re.compile(
    r'<tr class=\"row\">[\s]*<td class=\"span2\"><strong>(.*)</strong>'
    r'</td>[\s]*<td class=\"span10\">(.*)</td>[\s]*</tr>'
)


def parse_wordlist(wordlist_url, sess):
    ''' parse html text and return the words in the page
    '''
    total_words = []
    page = 1
    while True:
        page_url = wordlist_url + '?page={}'.format(page)
        html = sess.get(page_url).text
        words = word_pattern.findall(html)
        if not words:
            break
        total_words.extend(words)
        page += 1
        print('page: {}'.format(page), end='\r')
    print('parse_wordlist({}) finished'.format(wordlist_url))
    return total_words


def parse_wordlist_with_explanation(wordlist_url, sess):
    ''' parse html text and return the words in the page
    '''
    total_words = {}
    page = 1
    while True:
        page_url = wordlist_url + '?page={}'.format(page)
        html = sess.get(page_url).text
        words = word_explanation_pattern.findall(html)
        if not words:
            break
        total_words.update(dict(words))
        page += 1
        print('page: {}'.format(page), end='\r')
    print('parse_wordlist({}) finished'.format(wordlist_url))
    return total_words


def parse_wordbook(wordbook_url, sess, explain=False):
    html = sess.get(wordbook_url).text

    wordbook = {}
    for url, wordlist_name in list_pattern.findall(html)[:-1]:
        wordlist_name = wordlist_name.strip()
        # the last match is a placeholder in JavaScript code
        if explain:
            words = parse_wordlist_with_explanation(root_url + url, sess)
        else:
            words = parse_wordlist(root_url + url, sess)

        while wordlist_name in wordbook:
            wordlist_name += '_'
        wordbook[wordlist_name] = words
    return wordbook


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-u', '--url',
                        help='Root url of the wordbook, e.g. '
                             'https://www.shanbay.com/wordlist/97051/')
    parser.add_argument('-o', '--output',
                        help='Output directory')
    parser.add_argument('-e', '--explain', default=False, action='store_true',
                        help='Also include explanation')
    FLAGS = parser.parse_args()
    with requests.Session() as sess:
        wordbook = parse_wordbook(FLAGS.url, sess, FLAGS.explain)

    if not op.isdir(FLAGS.output):
        os.mkdir(FLAGS.output)

    for name, wordlist in wordbook.items():
        json.dump(wordlist,
                  open(op.join(FLAGS.output, name + '.json'), 'w'),
                  indent=4,
                  ensure_ascii=False)
