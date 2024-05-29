import argparse
from pathlib import Path
import json

from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# TODO: Experiment with stemmers

nltk.download('punkt')
nltk.download('stopwords')


def clean_text(text: str) -> list:
    # Tokenize words, remove punctuation and stopwords, and stem words
    stop_words = set(stopwords.words('english'))
    # stemmer = PorterStemmer()

    words = word_tokenize(text)
    cleaned_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]

    return cleaned_words


def clean_text_sent(text: str) -> list:
    # Tokenize sentences
    sentences = sent_tokenize(text)

    # Tokenize words, remove punctuation and stopwords, and stem words
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    cleaned_text = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        cleaned_words = [stemmer.stem(word) for word in words if word.isalnum() and word.lower() not in stop_words]
        cleaned_text.append(cleaned_words)

    return cleaned_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decade', type=str, required=True)
    parser.add_argument('-n', '--num', type=str, required=True)
    args = parser.parse_args(['-d', '2020', '-n', '1'])
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