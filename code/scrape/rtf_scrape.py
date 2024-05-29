from pathlib import Path
import re
import json
import argparse

from striprtf.striprtf import rtf_to_text
from tqdm import tqdm

from metadata_parser import proc_meta
from token_cleaning import clean_text


def proc_rtf(path: Path) -> dict:
    with open(path, 'r') as in_file:
        txt = rtf_to_text(in_file.read())

    body_split = re.split(r'\nBody\n', txt)
    meta = re.sub(r'\n+', '\n', body_split[0]).strip()
    body = re.split(r'\nLoad-Date', body_split[1])[0]
    body = re.sub(r'\n', ' ', body).strip()

    meta_lines = [line for line in meta.splitlines() if line != ' ']

    return {'meta': proc_meta(meta_lines), 'body': clean_text(body)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--term', default='disab', type=str)
    parser.add_argument('-d', '--decade', type=str, required=True)
    parser.add_argument('-n', '--nums', type=str, required=True, nargs='+')
    args = parser.parse_args()
    term = args.term
    decade = args.decade
    nums = args.nums
    for num in nums:
        name = f'{decade}s-{num}{term[0]}'
        print(name)
        root_path = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/{term}/{decade}s/{name}')
        rtf_files = [f for f in root_path.rglob('*.rtf') if '_doclist' not in f.name]
        print(f'Found {len(rtf_files)} rtfs')

        data = [proc_rtf(p) for p in tqdm(rtf_files)]

        out_path = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/{term}/{decade}s/json')
        out_path /= f'{name}.json'
        with open(out_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
            print(f'Wrote to {out_path}')
