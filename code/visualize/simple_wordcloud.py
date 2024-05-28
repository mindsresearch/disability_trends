import argparse
from pathlib import Path
import json

import matplotlib.pyplot as plt
from wordcloud import WordCloud

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decade', type=str, required=True)
    args = parser.parse_args()
    decade = args.decade
    json_paths = list(Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/disab/{decade}s/json').glob('*.json'))
    print(f'Found {len(json_paths)} json files')

    bodies = []
    for file in json_paths:
        with open(file, 'r') as f:
            data = json.load(f)
        for d in data:
            bodies.append(d['body'])
    bodies = ' '.join(bodies)
    wc = WordCloud().generate(bodies)

    plt.imshow(wc, interpolation='bilinear')
    plt.title(f'wordcloud for {decade}s')
    plt.axis("off")
    plt.show()
