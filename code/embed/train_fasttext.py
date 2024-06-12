import argparse
from pathlib import Path
import json

from gensim.models import FastText

# from nltk.stem import PorterStemmer

# !!! WARNING !!!
#
# Due to depreciation issues, you will need to modify gensim/matutils.py as follows:
# 1. Remove the triu import from scipy.linalg
# 2. Where triu is called, change it to `np.triu`

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--term', default='disab', type=str)
parser.add_argument('-d', '--decade', type=str, required=True)
args = parser.parse_args(['-t', 'disab', '-d', '1990'])
term = args.term
decade = args.decade
# json_paths = list(Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/{term}/{decade}s/json').glob('*.json'))
script_loc = Path(__file__).resolve()
data_path = script_loc.parent.parent/'data'
json_path = data_path / term / f'{decade}s' / 'json'
json_paths = list(json_path.rglob('*.json'))
print(f'Found {len(json_paths)} json files')

bodies = []
for file in json_paths:
    with open(file, 'r') as f:
        data = json.load(f)
    for d in data:
        bodies.append(d['body'])

print('training model...')
model = FastText(sentences=bodies, vector_size=100, window=5, min_count=1, epochs=10)

print('saving model...')
model.save(str(json_path/'fasttext_model.bin'))

# Example usage
#
# s = PorterStemmer()
keys = ['disability']
for k in keys:
    # k = s.stem(k)
    word_vector = model.wv[k]
    print(f'\n====== {k} ======')
    print(word_vector)
