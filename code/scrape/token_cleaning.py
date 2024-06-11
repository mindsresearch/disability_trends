import argparse
from pathlib import Path
import json

from tqdm import tqdm
import stanza
stanza.download('en')
NLPL = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
# TODO: Experiment with stemmers


def lemma_warn():
    # lemmatizer = WordNetLemmatizer()
    print('====== WARNING ======')
    print('You are using a lemmatized version of your text!')
    # print('Here is a cheat sheet for what terms to use:')
    # cheat_terms = ['disabled', 'disability', 'neurodivergent', 'autistic', 'autism', 'handicapped', 'golf', 'sports']
    # for term in cheat_terms:
    #     print(f'  {term}: {lemmatizer.lemmatize(term)}')
    print('=====================')


def clean_text(text: str) -> list:
    doc = NLPL(text)
    return [w.lemma for s in doc.sentences for w in s.words]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decade', type=str, required=True)
    parser.add_argument('-n', '--num', type=str, required=True)
    args = parser.parse_args()
    decade = args.decade
    num = args.num
    name = f'{decade}s-{num}'
    json_path = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/disab/{decade}s/json/{name}.json')
    data = json.load(json_path.open())
    for d in tqdm(data):
        d['body'] = clean_text(d['body'])
    out_file = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/disab/{decade}s/json/{name}.json')
    with open(out_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Saved {out_file}')
