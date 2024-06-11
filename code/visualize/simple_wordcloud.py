import argparse
from pathlib import Path
import json

import matplotlib.pyplot as plt
from wordcloud import WordCloud

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--term', default='disab', type=str)
    parser.add_argument('-d', '--decade', type=str, required=True)
    args = parser.parse_args(['-t', 'handicap', '-d', '2020'])
    term = args.term
    decade = args.decade
    script_loc = Path(__file__).resolve()
    data_path = script_loc.parent.parent / 'data'
    json_path = data_path / term / f'{decade}s' / 'json'
    json_paths = list(json_path.rglob('*.json'))
    print(f'Found {len(json_paths)} json files')

    bodies = []
    for file in json_paths:
        with open(file, 'r') as f:
            data = json.load(f)
        for d in data:
            bodies.append(' '.join(d['body']))
    bodies = ' '.join(bodies)
    wc = WordCloud().generate(bodies)

    plt.imshow(wc, interpolation='bilinear')
    plt.title(f'{term} wordcloud for {decade}s')
    plt.axis("off")
    plt.show()
