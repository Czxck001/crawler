''' Grab the Barron 800 high-frequency word list
'''
import re
import json
import requests

barron_url = r'https://quizlet.com/6876275/'\
    r'barrons-800-high-frequency-gre-word-list-flash-cards/'

pattern = re.compile(
    '<div class="SetPage-term">'
    '<div class="SetPageTerm">'
    '<div class="SetPageTerm-inner">'
    '<div class="SetPageTerm-contentWrapper">'
    '<div class="SetPageTerm-content">'
    '<div class="SetPageTerm-word">'
    '<div class="SetPageTerm-wordText">'
    '<span class="TermText notranslate lang-en">'
    '([A-Z]*)'
    '</span></div></div>'
    '<div class="SetPageTerm-definition">'
    '<div class="SetPageTerm-definitionText">'
    '<span class="TermText notranslate lang-en">'
    '([A-Z,; ]*)'
    '</span></div></div></div></div></div></div></div>'
)


def parse_wordlist(url):
    html = requests.get(url).text
    results = pattern.findall(html)
    return [
        {
            'word': word.lower(),
            'definition': defi.lower()
        }
        for word, defi in results
    ]


if __name__ == '__main__':
    print(json.dumps(parse_wordlist(barron_url), indent=4))
